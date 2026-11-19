<?php
/**
 * Post type, taxonomy, and meta registration.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Registers the checklist item post type, its category taxonomy, and item meta.
 */
class CodTracker_Content {

	public const POST_TYPE = 'codt_item';
	public const TAXONOMY  = 'codt_category';

	/**
	 * Item text meta keys and their sanitize callbacks.
	 *
	 * @var array<string, string>
	 */
	public const META = array(
		'codt_requirement' => 'sanitize_textarea_field',
		'codt_reward'      => 'sanitize_textarea_field',
		'codt_location'    => 'sanitize_text_field',
		'codt_sources'     => 'sanitize_textarea_field',
		'codt_key'         => 'sanitize_text_field',
	);

	/**
	 * Hook registration.
	 *
	 * @return void
	 */
	public static function init(): void {
		add_action( 'init', array( __CLASS__, 'register' ) );
	}

	/**
	 * Register the post type, taxonomy, and meta.
	 *
	 * @return void
	 */
	public static function register(): void {
		register_post_type(
			self::POST_TYPE,
			array(
				'labels'       => array(
					'name'          => __( 'DMZ Checklist', 'codtracker' ),
					'singular_name' => __( 'Checklist Item', 'codtracker' ),
					'add_new_item'  => __( 'Add Checklist Item', 'codtracker' ),
					'edit_item'     => __( 'Edit Checklist Item', 'codtracker' ),
					'all_items'     => __( 'All Items', 'codtracker' ),
					'menu_name'     => __( 'DMZ Tracker', 'codtracker' ),
				),
				'public'       => false,
				'show_ui'      => true,
				'show_in_rest' => true,
				'menu_icon'    => 'dashicons-yes-alt',
				'supports'     => array( 'title', 'editor', 'page-attributes' ),
			)
		);

		register_taxonomy(
			self::TAXONOMY,
			self::POST_TYPE,
			array(
				'labels'            => array(
					'name'          => __( 'Categories', 'codtracker' ),
					'singular_name' => __( 'Category', 'codtracker' ),
				),
				'hierarchical'      => true,
				'public'            => false,
				'show_ui'           => true,
				'show_in_rest'      => true,
				'show_admin_column' => true,
			)
		);

		register_term_meta(
			self::TAXONOMY,
			'codt_order',
			array(
				'type'              => 'integer',
				'single'            => true,
				'default'           => 0,
				'show_in_rest'      => true,
				'sanitize_callback' => 'absint',
			)
		);

		foreach ( self::META as $key => $sanitize ) {
			register_post_meta(
				self::POST_TYPE,
				$key,
				array(
					'type'              => 'string',
					'single'            => true,
					'show_in_rest'      => true,
					'sanitize_callback' => $sanitize,
					'auth_callback'     => array( __CLASS__, 'can_edit' ),
				)
			);
		}

		register_post_meta(
			self::POST_TYPE,
			'codt_goal',
			array(
				'type'              => 'integer',
				'single'            => true,
				'default'           => 1,
				'show_in_rest'      => true,
				'sanitize_callback' => array( __CLASS__, 'sanitize_goal' ),
				'auth_callback'     => array( __CLASS__, 'can_edit' ),
			)
		);

		register_post_meta(
			self::POST_TYPE,
			'codt_confirmed',
			array(
				'type'              => 'boolean',
				'single'            => true,
				'default'           => false,
				'show_in_rest'      => true,
				'sanitize_callback' => 'rest_sanitize_boolean',
				'auth_callback'     => array( __CLASS__, 'can_edit' ),
			)
		);
	}

	/**
	 * Clamp an item's completion goal to 1..99.
	 *
	 * @param mixed $value Raw value.
	 * @return int
	 */
	public static function sanitize_goal( $value ): int {
		return max( 1, min( 99, absint( $value ) ) );
	}

	/**
	 * Meta auth callback.
	 *
	 * @return bool
	 */
	public static function can_edit(): bool {
		return current_user_can( 'edit_posts' );
	}

	/**
	 * Build the category tree with published items attached, ordered for display.
	 *
	 * @param array<int, array<int, int>> $user_order Optional per-user order, parent term ID => child term IDs.
	 * @return array<int, array<string, mixed>> Top-level category nodes.
	 */
	public static function get_tree( array $user_order = array() ): array {
		$terms = get_terms(
			array(
				'taxonomy'   => self::TAXONOMY,
				'hide_empty' => false,
			)
		);

		if ( is_wp_error( $terms ) || empty( $terms ) ) {
			return array();
		}

		$nodes = array();
		foreach ( $terms as $term ) {
			$nodes[ $term->term_id ] = array(
				'term'     => $term,
				'order'    => (int) get_term_meta( $term->term_id, 'codt_order', true ),
				'items'    => array(),
				'children' => array(),
			);
		}

		// One query for every item; WP_Query primes term and meta caches in bulk.
		$items = get_posts(
			array(
				'post_type'        => self::POST_TYPE,
				'post_status'      => 'publish',
				'posts_per_page'   => -1,
				'orderby'          => array(
					'menu_order' => 'ASC',
					'title'      => 'ASC',
				),
				'suppress_filters' => false,
			)
		);

		foreach ( $items as $item ) {
			$item_terms = get_the_terms( $item, self::TAXONOMY );
			if ( empty( $item_terms ) || is_wp_error( $item_terms ) ) {
				continue;
			}
			$term_id = $item_terms[0]->term_id;
			if ( isset( $nodes[ $term_id ] ) ) {
				$nodes[ $term_id ]['items'][] = $item;
			}
		}

		// Attach children by reference so nested additions propagate up.
		$roots = array();
		foreach ( $nodes as &$node ) {
			$parent = $node['term']->parent;
			if ( $parent && isset( $nodes[ $parent ] ) ) {
				$nodes[ $parent ]['children'][] = &$node;
			} else {
				$roots[] = &$node;
			}
		}
		unset( $node );

		self::sort_nodes( $roots );

		if ( $user_order ) {
			self::apply_user_order( $roots, $user_order, 0 );
		}

		return $roots;
	}

	/**
	 * Recursively reorder sibling nodes by a user's saved order.
	 *
	 * Sections in the saved list fill the slots that listed sections held in the default order;
	 * sections not in the list (e.g. added later) stay in their default slot.
	 *
	 * @param array<int, array<string, mixed>> $nodes      Sibling nodes, already in default order.
	 * @param array<int, array<int, int>>      $user_order Parent term ID => ordered child term IDs.
	 * @param int                              $parent_id  Parent term ID of these siblings (0 = top level).
	 * @return void
	 */
	private static function apply_user_order( array &$nodes, array $user_order, int $parent_id ): void {
		if ( ! empty( $user_order[ $parent_id ] ) ) {
			$rank   = array_flip( $user_order[ $parent_id ] );
			$listed = array_values(
				array_filter( $nodes, static fn( array $node ): bool => isset( $rank[ $node['term']->term_id ] ) )
			);
			usort(
				$listed,
				static fn( array $a, array $b ): int => $rank[ $a['term']->term_id ] <=> $rank[ $b['term']->term_id ]
			);

			$merged = array();
			$next   = 0;
			foreach ( $nodes as $node ) {
				$merged[] = isset( $rank[ $node['term']->term_id ] ) ? $listed[ $next++ ] : $node;
			}
			$nodes = $merged;
		}

		foreach ( $nodes as &$node ) {
			self::apply_user_order( $node['children'], $user_order, (int) $node['term']->term_id );
		}
		unset( $node );
	}

	/**
	 * Recursively sort category nodes by order, then name, and record each node's default position.
	 *
	 * @param array<int, array<string, mixed>> $nodes Nodes to sort in place.
	 * @return void
	 */
	private static function sort_nodes( array &$nodes ): void {
		usort(
			$nodes,
			static fn( array $a, array $b ): int => array( $a['order'], $a['term']->name ) <=> array( $b['order'], $b['term']->name )
		);
		foreach ( $nodes as $index => &$node ) {
			$node['default_index'] = $index;
			self::sort_nodes( $node['children'] );
		}
		unset( $node );
	}
}
