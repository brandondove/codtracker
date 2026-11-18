<?php
/**
 * Login gating: the front page is the login screen, the tracker requires a login.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Sends logged-in visitors from the front page to the tracker, sends logged-out
 * visitors from any page containing the checklist block to the front page, and
 * lands non-editors on the tracker after logging in.
 */
class CodTracker_Access {

	/**
	 * Hook registration.
	 *
	 * @return void
	 */
	public static function init(): void {
		add_action( 'template_redirect', array( __CLASS__, 'gate' ) );
		add_filter( 'login_redirect', array( __CLASS__, 'login_redirect' ), 10, 3 );
		add_filter( 'login_form_bottom', array( __CLASS__, 'form_links' ) );
	}

	/**
	 * URL of the tracker page, or an empty string if it does not exist.
	 *
	 * @return string
	 */
	public static function tracker_url(): string {
		/**
		 * Filters the slug of the page that holds the checklist block.
		 *
		 * @param string $slug Page slug. Default 'tracker'.
		 */
		$slug = (string) apply_filters( 'codt_tracker_page_slug', 'tracker' );
		$page = get_page_by_path( $slug );

		if ( ! $page instanceof WP_Post || 'publish' !== $page->post_status ) {
			return '';
		}

		return (string) get_permalink( $page );
	}

	/**
	 * Redirect between the front page (login) and the tracker based on login state.
	 *
	 * @return void
	 */
	public static function gate(): void {
		if ( is_user_logged_in() ) {
			if ( is_front_page() ) {
				$tracker = self::tracker_url();
				if ( '' !== $tracker ) {
					wp_safe_redirect( $tracker );
					exit;
				}
			}
			return;
		}

		if ( is_singular() && ! is_front_page() && has_block( 'codt/checklist', get_queried_object_id() ) ) {
			wp_safe_redirect( home_url( '/' ) );
			exit;
		}
	}

	/**
	 * Send users who can't edit content to the tracker after logging in.
	 *
	 * Only replaces WordPress's default destination (wp-admin); an explicit
	 * redirect_to is respected. Editors and admins keep the default.
	 *
	 * @param string           $redirect_to           Destination URL.
	 * @param string           $requested_redirect_to Destination requested via redirect_to.
	 * @param WP_User|WP_Error $user                  User that logged in, or an error.
	 * @return string
	 */
	public static function login_redirect( $redirect_to, $requested_redirect_to, $user ): string {
		if ( ! $user instanceof WP_User || $user->has_cap( 'edit_posts' ) ) {
			return (string) $redirect_to;
		}

		if ( '' !== (string) $requested_redirect_to && admin_url() !== $requested_redirect_to ) {
			return (string) $redirect_to;
		}

		$tracker = self::tracker_url();

		return '' !== $tracker ? $tracker : (string) $redirect_to;
	}

	/**
	 * Add "Register" and "Lost your password?" links under front-end login forms.
	 *
	 * @param string $content Existing markup after the form fields.
	 * @return string
	 */
	public static function form_links( $content ): string {
		$links = array();

		if ( get_option( 'users_can_register' ) ) {
			$links[] = sprintf( '<a href="%s">%s</a>', esc_url( wp_registration_url() ), esc_html__( 'Register', 'codtracker' ) );
		}
		$links[] = sprintf( '<a href="%s">%s</a>', esc_url( wp_lostpassword_url() ), esc_html__( 'Lost your password?', 'codtracker' ) );

		return (string) $content . '<p class="codt-login-links">' . implode( ' | ', $links ) . '</p>';
	}
}
