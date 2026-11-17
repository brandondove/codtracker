<?php
/**
 * Imports categories and items from a seed JSON file.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Idempotent importer. Items are matched on a stable codt_key (category/title-slug),
 * so re-running updates existing items instead of duplicating them.
 */
class CodTracker_Seeder {

	/**
	 * Run the import.
	 *
	 * @param string $file Absolute path to seed JSON.
	 * @return array{categories:int, created:int, updated:int, skipped:string[]}|WP_Error
	 */
	public static function import( string $file ) {
		if ( ! is_readable( $file ) ) {
			return new WP_Error( 'codt_seed_missing', sprintf( 'Seed file not readable: %s', $file ) );
		}

		$data = json_decode( (string) file_get_contents( $file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents -- Local file.
		if ( ! is_array( $data ) || empty( $data['categories'] ) || ! isset( $data['items'] ) ) {
			return new WP_Error( 'codt_seed_invalid', 'Seed file must contain "categories" and "items".' );
		}

		$term_ids = array();
		foreach ( $data['categories'] as $cat ) {
			$slug   = sanitize_title( $cat['slug'] ?? '' );
			$parent = ! empty( $cat['parent'] ) ? ( $term_ids[ sanitize_title( $cat['parent'] ) ] ?? 0 ) : 0;
			if ( '' === $slug ) {
				continue;
			}

			$args     = array(
				'slug'        => $slug,
				'parent'      => $parent,
				'description' => sanitize_textarea_field( $cat['description'] ?? '' ),
			);
			$existing = get_term_by( 'slug', $slug, CodTracker_Content::TAXONOMY );
			if ( $existing ) {
				$args['name'] = sanitize_text_field( $cat['name'] ?? $slug );
				wp_update_term( $existing->term_id, CodTracker_Content::TAXONOMY, $args );
				$term_id = $existing->term_id;
			} else {
				$result = wp_insert_term( sanitize_text_field( $cat['name'] ?? $slug ), CodTracker_Content::TAXONOMY, $args );
				if ( is_wp_error( $result ) ) {
					continue;
				}
				$term_id = (int) $result['term_id'];
			}

			update_term_meta( $term_id, 'codt_order', absint( $cat['order'] ?? 0 ) );
			$term_ids[ $slug ] = (int) $term_id;
		}

		$created = 0;
		$updated = 0;
		$skipped = array();

		foreach ( $data['items'] as $item ) {
			$title    = sanitize_text_field( $item['title'] ?? '' );
			$category = sanitize_title( $item['category'] ?? '' );
			if ( '' === $title || ! isset( $term_ids[ $category ] ) ) {
				$skipped[] = $title ?: '(untitled)';
				continue;
			}

			$key      = $category . '/' . sanitize_title( $title );
			$existing = get_posts(
				array(
					'post_type'      => CodTracker_Content::POST_TYPE,
					'post_status'    => 'any',
					'posts_per_page' => 1,
					'fields'         => 'ids',
					'meta_key'       => 'codt_key', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key -- One-off CLI import.
					'meta_value'     => $key, // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_value -- One-off CLI import.
				)
			);

			$postarr = array(
				'post_type'    => CodTracker_Content::POST_TYPE,
				'post_status'  => 'publish',
				'post_title'   => $title,
				'post_content' => sanitize_textarea_field( $item['description'] ?? '' ),
				'menu_order'   => absint( $item['order'] ?? 0 ),
			);

			if ( $existing ) {
				$postarr['ID'] = $existing[0];
				$post_id       = wp_update_post( $postarr, true );
				++$updated;
			} else {
				$post_id = wp_insert_post( $postarr, true );
				++$created;
			}

			if ( is_wp_error( $post_id ) ) {
				$skipped[] = $title;
				continue;
			}

			wp_set_object_terms( $post_id, $term_ids[ $category ], CodTracker_Content::TAXONOMY );
			update_post_meta( $post_id, 'codt_key', $key );
			update_post_meta( $post_id, 'codt_requirement', sanitize_textarea_field( $item['requirement'] ?? '' ) );
			update_post_meta( $post_id, 'codt_reward', sanitize_textarea_field( $item['reward'] ?? '' ) );
			update_post_meta( $post_id, 'codt_location', sanitize_text_field( $item['location'] ?? '' ) );
			update_post_meta( $post_id, 'codt_sources', implode( "\n", array_map( 'esc_url_raw', (array) ( $item['sources'] ?? array() ) ) ) );
			update_post_meta( $post_id, 'codt_confirmed', ! empty( $item['confirmed'] ) );
			update_post_meta( $post_id, 'codt_goal', CodTracker_Content::sanitize_goal( $item['goal'] ?? 1 ) );
		}

		return array(
			'categories' => count( $term_ids ),
			'created'    => $created,
			'updated'    => $updated,
			'skipped'    => $skipped,
		);
	}

	/**
	 * Find imported items whose key is no longer in the seed file.
	 *
	 * Only items carrying a codt_key (i.e. created by the importer) are considered,
	 * so items added by hand in wp-admin are never returned.
	 *
	 * @param string $file Absolute path to seed JSON.
	 * @return array<int, string>|WP_Error Post ID => codt_key.
	 */
	public static function find_orphans( string $file ) {
		if ( ! is_readable( $file ) ) {
			return new WP_Error( 'codt_seed_missing', sprintf( 'Seed file not readable: %s', $file ) );
		}

		$data = json_decode( (string) file_get_contents( $file ), true ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents -- Local file.
		if ( ! is_array( $data ) || ! isset( $data['items'] ) || ! is_array( $data['items'] ) ) {
			return new WP_Error( 'codt_seed_invalid', 'Seed file must contain "items".' );
		}

		// Guard against wiping everything because of an empty or truncated seed.
		if ( empty( $data['items'] ) ) {
			return new WP_Error( 'codt_seed_empty', 'Seed file has no items; refusing to prune.' );
		}

		$seed_keys = array();
		foreach ( $data['items'] as $item ) {
			$seed_keys[ sanitize_title( $item['category'] ?? '' ) . '/' . sanitize_title( $item['title'] ?? '' ) ] = true;
		}

		$post_ids = get_posts(
			array(
				'post_type'      => CodTracker_Content::POST_TYPE,
				'post_status'    => array( 'publish', 'draft', 'pending', 'private', 'future' ),
				'posts_per_page' => -1,
				'fields'         => 'ids',
				'meta_key'       => 'codt_key', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key -- One-off CLI maintenance.
				'meta_compare'   => 'EXISTS',
			)
		);

		$orphans = array();
		foreach ( $post_ids as $post_id ) {
			$key = (string) get_post_meta( $post_id, 'codt_key', true );
			if ( '' !== $key && ! isset( $seed_keys[ $key ] ) ) {
				$orphans[ (int) $post_id ] = $key;
			}
		}

		return $orphans;
	}
}
