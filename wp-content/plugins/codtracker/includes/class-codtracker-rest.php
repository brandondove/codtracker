<?php
/**
 * REST endpoints for reading and saving progress.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Registers codt/v1/progress. Cookie auth requires the wp_rest nonce in X-WP-Nonce.
 */
class CodTracker_Rest {

	public const NAMESPACE = 'codt/v1';

	/**
	 * Hook registration.
	 *
	 * @return void
	 */
	public static function init(): void {
		add_action( 'rest_api_init', array( __CLASS__, 'register_routes' ) );
	}

	/**
	 * Register routes.
	 *
	 * @return void
	 */
	public static function register_routes(): void {
		register_rest_route(
			self::NAMESPACE,
			'/progress',
			array(
				array(
					'methods'             => WP_REST_Server::READABLE,
					'callback'            => array( __CLASS__, 'get_progress' ),
					'permission_callback' => 'is_user_logged_in',
				),
				array(
					'methods'             => WP_REST_Server::EDITABLE,
					'callback'            => array( __CLASS__, 'update_progress' ),
					'permission_callback' => 'is_user_logged_in',
					'args'                => array(
						'item_id'   => array(
							'type'              => 'integer',
							'required'          => true,
							'minimum'           => 1,
							'validate_callback' => array( __CLASS__, 'validate_item' ),
						),
						'count'     => array(
							'description' => 'Completions so far, clamped to the item goal.',
							'type'        => 'integer',
							'minimum'     => 0,
						),
						'collected' => array(
							'description' => 'Shorthand: true sets count to the goal, false to 0.',
							'type'        => 'boolean',
						),
					),
				),
			)
		);

		register_rest_route(
			self::NAMESPACE,
			'/progress/bulk',
			array(
				'methods'             => WP_REST_Server::CREATABLE,
				'callback'            => array( __CLASS__, 'update_progress_bulk' ),
				'permission_callback' => 'is_user_logged_in',
				'args'                => array(
					'item_ids'  => array(
						'description'       => 'Checklist item IDs to update.',
						'type'              => 'array',
						'items'             => array(
							'type'    => 'integer',
							'minimum' => 1,
						),
						'minItems'          => 1,
						'maxItems'          => 500,
						'required'          => true,
						'validate_callback' => array( __CLASS__, 'validate_items' ),
					),
					'collected' => array(
						'description' => 'True sets each item to its goal, false clears it.',
						'type'        => 'boolean',
						'required'    => true,
					),
				),
			)
		);
	}

	/**
	 * Validate the item_ids schema, then ensure every ID is a published checklist item.
	 *
	 * @param mixed           $value   Item IDs.
	 * @param WP_REST_Request $request Request.
	 * @param string          $param   Parameter name.
	 * @return true|WP_Error
	 */
	public static function validate_items( $value, WP_REST_Request $request, string $param ) {
		$valid = rest_validate_request_arg( $value, $request, $param );
		if ( true !== $valid ) {
			return $valid;
		}

		$ids = array_map( 'absint', (array) $value );
		_prime_post_caches( $ids, false, true );

		foreach ( $ids as $id ) {
			$item = self::validate_item( $id );
			if ( true !== $item ) {
				return $item;
			}
		}
		return true;
	}

	/**
	 * Ensure the ID is a published checklist item.
	 *
	 * @param mixed $value Item ID.
	 * @return true|WP_Error
	 */
	public static function validate_item( $value ) {
		$post = get_post( absint( $value ) );
		if ( ! $post || CodTracker_Content::POST_TYPE !== $post->post_type || 'publish' !== $post->post_status ) {
			return new WP_Error( 'codt_invalid_item', __( 'Unknown checklist item.', 'codtracker' ), array( 'status' => 404 ) );
		}
		return true;
	}

	/**
	 * GET handler.
	 *
	 * @return WP_REST_Response
	 */
	public static function get_progress(): WP_REST_Response {
		return rest_ensure_response( array( 'progress' => (object) CodTracker_Progress::get( get_current_user_id() ) ) );
	}

	/**
	 * POST handler.
	 *
	 * @param WP_REST_Request $request Request.
	 * @return WP_REST_Response|WP_Error
	 */
	public static function update_progress( WP_REST_Request $request ) {
		$item_id = (int) $request['item_id'];

		if ( null !== $request['count'] ) {
			$count = (int) $request['count'];
		} elseif ( null !== $request['collected'] ) {
			$count = $request['collected'] ? CodTracker_Progress::goal( $item_id ) : 0;
		} else {
			return new WP_Error( 'codt_missing_value', __( 'Provide count or collected.', 'codtracker' ), array( 'status' => 400 ) );
		}

		$counts = CodTracker_Progress::set( get_current_user_id(), $item_id, $count );
		return rest_ensure_response( array( 'progress' => (object) $counts ) );
	}

	/**
	 * Bulk POST handler: mark every listed item collected or cleared in one write.
	 *
	 * @param WP_REST_Request $request Request.
	 * @return WP_REST_Response
	 */
	public static function update_progress_bulk( WP_REST_Request $request ): WP_REST_Response {
		$ids    = array_values( array_unique( array_map( 'absint', (array) $request['item_ids'] ) ) );
		$counts = CodTracker_Progress::set_many( get_current_user_id(), $ids, (bool) $request['collected'] );
		return rest_ensure_response( array( 'progress' => (object) $counts ) );
	}
}
