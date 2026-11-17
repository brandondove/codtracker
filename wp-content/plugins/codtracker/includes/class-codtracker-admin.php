<?php
/**
 * Admin meta box and term order field.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Admin UI for editing checklist item details and category order.
 */
class CodTracker_Admin {

	private const NONCE_ACTION = 'codt_save_item';
	private const NONCE_FIELD  = 'codt_item_nonce';

	/**
	 * Hook registration.
	 *
	 * @return void
	 */
	public static function init(): void {
		add_action( 'add_meta_boxes_' . CodTracker_Content::POST_TYPE, array( __CLASS__, 'add_meta_box' ) );
		add_action( 'save_post_' . CodTracker_Content::POST_TYPE, array( __CLASS__, 'save' ) );
		add_action( CodTracker_Content::TAXONOMY . '_add_form_fields', array( __CLASS__, 'term_add_field' ) );
		add_action( CodTracker_Content::TAXONOMY . '_edit_form_fields', array( __CLASS__, 'term_edit_field' ) );
		add_action( 'created_' . CodTracker_Content::TAXONOMY, array( __CLASS__, 'save_term' ) );
		add_action( 'edited_' . CodTracker_Content::TAXONOMY, array( __CLASS__, 'save_term' ) );
	}

	/**
	 * Register the details meta box.
	 *
	 * @return void
	 */
	public static function add_meta_box(): void {
		add_meta_box( 'codt_details', __( 'Item Details', 'codtracker' ), array( __CLASS__, 'render_meta_box' ), CodTracker_Content::POST_TYPE, 'normal', 'high' );
	}

	/**
	 * Render the details meta box.
	 *
	 * @param WP_Post $post Current post.
	 * @return void
	 */
	public static function render_meta_box( WP_Post $post ): void {
		wp_nonce_field( self::NONCE_ACTION, self::NONCE_FIELD );

		$fields = array(
			'codt_requirement' => array( __( 'How to unlock / complete', 'codtracker' ), 'textarea' ),
			'codt_reward'      => array( __( 'Reward', 'codtracker' ), 'textarea' ),
			'codt_location'    => array( __( 'Location', 'codtracker' ), 'text' ),
			'codt_sources'     => array( __( 'Source URLs (one per line)', 'codtracker' ), 'textarea' ),
		);

		echo '<table class="form-table" role="presentation">';
		foreach ( $fields as $key => [ $label, $type ] ) {
			$value = (string) get_post_meta( $post->ID, $key, true );
			printf( '<tr><th scope="row"><label for="%1$s">%2$s</label></th><td>', esc_attr( $key ), esc_html( $label ) );
			if ( 'textarea' === $type ) {
				printf( '<textarea class="large-text" rows="3" id="%1$s" name="%1$s">%2$s</textarea>', esc_attr( $key ), esc_textarea( $value ) );
			} else {
				printf( '<input type="text" class="large-text" id="%1$s" name="%1$s" value="%2$s" />', esc_attr( $key ), esc_attr( $value ) );
			}
			echo '</td></tr>';
		}
		printf(
			'<tr><th scope="row"><label for="codt_goal">%1$s</label></th><td><input type="number" min="1" max="99" id="codt_goal" name="codt_goal" value="%2$d" class="small-text" /> <span class="description">%3$s</span></td></tr>',
			esc_html__( 'Times to complete', 'codtracker' ),
			CodTracker_Progress::goal( $post->ID ),
			esc_html__( '1 shows a checkbox; more shows a counter (e.g. 3 weapon manual extractions).', 'codtracker' )
		);
		printf(
			'<tr><th scope="row">%1$s</th><td><label><input type="checkbox" name="codt_confirmed" value="1" %2$s /> %3$s</label></td></tr>',
			esc_html__( 'Confirmed', 'codtracker' ),
			checked( (bool) get_post_meta( $post->ID, 'codt_confirmed', true ), true, false ),
			esc_html__( 'Verified by multiple or official sources', 'codtracker' )
		);
		echo '</table>';
	}

	/**
	 * Save meta box values.
	 *
	 * @param int $post_id Post ID.
	 * @return void
	 */
	public static function save( int $post_id ): void {
		if ( ! isset( $_POST[ self::NONCE_FIELD ] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST[ self::NONCE_FIELD ] ) ), self::NONCE_ACTION ) ) {
			return;
		}
		if ( wp_is_post_autosave( $post_id ) || ! current_user_can( 'edit_post', $post_id ) ) {
			return;
		}

		foreach ( array( 'codt_requirement', 'codt_reward', 'codt_location', 'codt_sources' ) as $key ) {
			if ( isset( $_POST[ $key ] ) ) {
				$sanitize = CodTracker_Content::META[ $key ];
				update_post_meta( $post_id, $key, $sanitize( wp_unslash( $_POST[ $key ] ) ) ); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput.InputNotSanitized -- Sanitized via mapped callback.
			}
		}
		if ( isset( $_POST['codt_goal'] ) ) {
			update_post_meta( $post_id, 'codt_goal', CodTracker_Content::sanitize_goal( sanitize_text_field( wp_unslash( $_POST['codt_goal'] ) ) ) );
		}
		update_post_meta( $post_id, 'codt_confirmed', ! empty( $_POST['codt_confirmed'] ) );
	}

	/**
	 * Order field on the add-term screen.
	 *
	 * @return void
	 */
	public static function term_add_field(): void {
		wp_nonce_field( 'codt_save_term', 'codt_term_nonce' );
		printf(
			'<div class="form-field"><label for="codt_order">%s</label><input type="number" name="codt_order" id="codt_order" value="0" min="0" /></div>',
			esc_html__( 'Display order', 'codtracker' )
		);
	}

	/**
	 * Order field on the edit-term screen.
	 *
	 * @param WP_Term $term Term being edited.
	 * @return void
	 */
	public static function term_edit_field( WP_Term $term ): void {
		wp_nonce_field( 'codt_save_term', 'codt_term_nonce' );
		printf(
			'<tr class="form-field"><th scope="row"><label for="codt_order">%1$s</label></th><td><input type="number" name="codt_order" id="codt_order" value="%2$d" min="0" /></td></tr>',
			esc_html__( 'Display order', 'codtracker' ),
			(int) get_term_meta( $term->term_id, 'codt_order', true )
		);
	}

	/**
	 * Save term order.
	 *
	 * @param int $term_id Term ID.
	 * @return void
	 */
	public static function save_term( int $term_id ): void {
		if ( ! isset( $_POST['codt_term_nonce'], $_POST['codt_order'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['codt_term_nonce'] ) ), 'codt_save_term' ) ) {
			return;
		}
		if ( ! current_user_can( 'manage_categories' ) ) {
			return;
		}
		update_term_meta( $term_id, 'codt_order', absint( $_POST['codt_order'] ) );
	}
}
