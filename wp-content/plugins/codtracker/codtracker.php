<?php
/**
 * Plugin Name:       CodTracker
 * Description:       Categorized checklist for tracking Call of Duty: Modern Warfare 4 DMZ unlocks, missions, and collectibles.
 * Version:           0.2.0
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

define( 'CODT_VERSION', '0.2.0' );
define( 'CODT_DIR', plugin_dir_path( __FILE__ ) );

require_once CODT_DIR . 'includes/class-codtracker-content.php';
require_once CODT_DIR . 'includes/class-codtracker-admin.php';
require_once CODT_DIR . 'includes/class-codtracker-progress.php';
require_once CODT_DIR . 'includes/class-codtracker-rest.php';
require_once CODT_DIR . 'includes/class-codtracker-seeder.php';

CodTracker_Content::init();
CodTracker_Admin::init();
CodTracker_Rest::init();

add_action( 'init', 'codt_register_blocks' );

/**
 * Register the checklist block from its block.json metadata.
 *
 * @return void
 */
function codt_register_blocks(): void {
	register_block_type( CODT_DIR . 'blocks/checklist' );
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
