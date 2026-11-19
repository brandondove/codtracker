<?php
/**
 * Plugin Name:       CodTracker
 * Description:       Categorized checklist for tracking Call of Duty: Modern Warfare 4 DMZ unlocks, missions, and collectibles.
 * Version:           0.3.1
 * Requires at least: 6.5
 * Requires PHP:      8.1
 * Author:            Pixel Jar
 * License:           GPL-2.0-or-later
 * Text Domain:       codtracker
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

define( 'CODT_VERSION', '0.3.1' );
define( 'CODT_DIR', plugin_dir_path( __FILE__ ) );

require_once CODT_DIR . 'includes/class-codtracker-content.php';
require_once CODT_DIR . 'includes/class-codtracker-admin.php';
require_once CODT_DIR . 'includes/class-codtracker-progress.php';
require_once CODT_DIR . 'includes/class-codtracker-section-order.php';
require_once CODT_DIR . 'includes/class-codtracker-rest.php';
require_once CODT_DIR . 'includes/class-codtracker-seeder.php';
require_once CODT_DIR . 'includes/class-codtracker-access.php';

CodTracker_Content::init();
CodTracker_Admin::init();
CodTracker_Rest::init();
CodTracker_Access::init();

add_action( 'init', 'codt_register_blocks' );

/**
 * Register the checklist block from its block.json metadata.
 *
 * @return void
 */
function codt_register_blocks(): void {
	register_block_type( CODT_DIR . 'blocks/checklist' );
}

add_action( 'wp_enqueue_scripts', 'codt_enqueue_theme_style' );
add_action( 'wp_head', 'codt_print_site_icons', 1 );
add_action( 'admin_head', 'codt_print_site_icons', 1 );
add_action( 'login_head', 'codt_print_site_icons', 1 );
add_filter( 'render_block', 'codt_render_site_logo', 10, 2 );

/**
 * Load the site-wide dark skin on the front end.
 *
 * @return void
 */
function codt_enqueue_theme_style(): void {
	wp_enqueue_style(
		'codt-theme',
		plugins_url( 'assets/css/theme.css', __FILE__ ),
		array(),
		CODT_VERSION
	);
}

/**
 * Print the favicon and touch icon.
 *
 * Assets live in the plugin so they deploy with it.
 *
 * @return void
 */
function codt_print_site_icons(): void {
	$version = CODT_VERSION;
	$svg     = add_query_arg( 'ver', $version, plugins_url( 'assets/brand/icon.svg', __FILE__ ) );
	$png     = add_query_arg( 'ver', $version, plugins_url( 'assets/brand/favicon-32.png', __FILE__ ) );
	$touch   = add_query_arg( 'ver', $version, plugins_url( 'assets/brand/apple-touch-icon.png', __FILE__ ) );

	printf(
		'<link rel="icon" href="%1$s" type="image/svg+xml" />' . "\n" .
		'<link rel="icon" href="%2$s" type="image/png" sizes="32x32" />' . "\n" .
		'<link rel="apple-touch-icon" href="%3$s" />' . "\n",
		esc_url( $svg ),
		esc_url( $png ),
		esc_url( $touch )
	);
}

/**
 * Replace the site title with the logo on the front end.
 *
 * @param string               $block_content Rendered block HTML.
 * @param array<string, mixed> $block         Parsed block.
 * @return string
 */
function codt_render_site_logo( string $block_content, array $block ): string {
	if ( ( $block['blockName'] ?? '' ) !== 'core/site-title' || is_admin() ) {
		return $block_content;
	}

	$level = isset( $block['attrs']['level'] ) ? (int) $block['attrs']['level'] : 0;
	$tag   = ( $level >= 1 && $level <= 6 ) ? 'h' . $level : 'p';
	$class = 'wp-block-site-title';

	if ( ! empty( $block['attrs']['textAlign'] ) ) {
		$class .= ' has-text-align-' . sanitize_html_class( (string) $block['attrs']['textAlign'] );
	}

	$current = is_front_page() ? ' aria-current="page"' : '';
	$name    = get_bloginfo( 'name', 'display' );

	return sprintf(
		'<%1$s class="%2$s"><a href="%3$s" rel="home" aria-label="%4$s"%5$s><img class="codt-logo" src="%6$s" alt="" width="434" height="88" decoding="async" /></a></%1$s>',
		$tag,
		esc_attr( $class ),
		esc_url( home_url( '/' ) ),
		esc_attr( $name ),
		$current,
		esc_url( plugins_url( 'assets/brand/logo.svg', __FILE__ ) )
	);
}

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	require_once CODT_DIR . 'includes/class-codtracker-cli.php';
	WP_CLI::add_command( 'codt', 'CodTracker_CLI' );
}

register_activation_hook( __FILE__, 'codt_activate' );

/**
 * Register content types and flush rewrite rules on activation.
 *
 * @return void
 */
function codt_activate(): void {
	CodTracker_Content::register();
	flush_rewrite_rules();
}

register_deactivation_hook( __FILE__, 'flush_rewrite_rules' );
