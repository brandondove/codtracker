<?php
/**
 * WP-CLI commands.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Manage the CodTracker DMZ checklist.
 */
class CodTracker_CLI {

	/**
	 * Import categories and items from a seed JSON file. Safe to re-run.
	 *
	 * ## OPTIONS
	 *
	 * [--file=<path>]
	 * : Seed file path. Defaults to the plugin's data/seed.json.
	 *
	 * [--prune]
	 * : After importing, move imported items that are no longer in the seed to the trash.
	 * Items added by hand in wp-admin (no seed key) are never touched.
	 *
	 * [--dry-run]
	 * : List the items --prune would remove, without importing or changing anything.
	 *
	 * ## EXAMPLES
	 *
	 *     wp codt seed
	 *     wp codt seed --prune --dry-run
	 *     wp codt seed --prune
	 *
	 * @param array<int, string>    $args       Positional args.
	 * @param array<string, string> $assoc_args Named args.
	 * @return void
	 */
	public function seed( array $args, array $assoc_args ): void {
		$file    = $assoc_args['file'] ?? CODT_DIR . 'data/seed.json';
		$prune   = (bool) WP_CLI\Utils\get_flag_value( $assoc_args, 'prune', false );
		$dry_run = (bool) WP_CLI\Utils\get_flag_value( $assoc_args, 'dry-run', false );

		if ( $dry_run ) {
			$this->report_orphans( $file, false );
			return;
		}

		$result = CodTracker_Seeder::import( $file );

		if ( is_wp_error( $result ) ) {
			WP_CLI::error( $result->get_error_message() );
		}

		WP_CLI::log( sprintf( 'Categories: %d', $result['categories'] ) );
		WP_CLI::log( sprintf( 'Items created: %d, updated: %d', $result['created'], $result['updated'] ) );
		if ( $result['skipped'] ) {
			WP_CLI::warning( 'Skipped (missing category or error): ' . implode( ', ', $result['skipped'] ) );
		}
		if ( $prune ) {
			$this->report_orphans( $file, true );
		}

		WP_CLI::success( 'Seed complete.' );
	}

	/**
	 * List orphaned items, optionally trashing them.
	 *
	 * @param string $file  Seed file path.
	 * @param bool   $trash Whether to move orphans to the trash.
	 * @return void
	 */
	private function report_orphans( string $file, bool $trash ): void {
		$orphans = CodTracker_Seeder::find_orphans( $file );
		if ( is_wp_error( $orphans ) ) {
			WP_CLI::error( $orphans->get_error_message() );
		}

		if ( ! $orphans ) {
			WP_CLI::log( 'Prune: no items to remove.' );
			return;
		}

		foreach ( $orphans as $post_id => $key ) {
			if ( $trash ) {
				$done = wp_trash_post( $post_id );
				WP_CLI::log( sprintf( '%s %d %s', $done ? 'Trashed' : 'Failed to trash', $post_id, $key ) );
			} else {
				WP_CLI::log( sprintf( 'Would trash %d %s', $post_id, $key ) );
			}
		}

		WP_CLI::log( sprintf( 'Prune: %d item(s) %s.', count( $orphans ), $trash ? 'moved to trash' : 'would be moved to trash (dry run)' ) );
	}
}
