<?php
/**
 * Per-user section order storage.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Stores each user's preferred section order in user meta, as parent_term_id => [child term IDs].
 * Top-level sections use parent 0. Sections missing from a saved list keep their default position.
 */
class CodTracker_Section_Order {

	public const META_KEY = 'codt_section_order';

	/**
	 * Get a user's saved section order.
	 *
	 * @param int $user_id User ID.
	 * @return array<int, array<int, int>> Parent term ID => ordered child term IDs.
	 */
	public static function get( int $user_id ): array {
		$raw = get_user_meta( $user_id, self::META_KEY, true );
		if ( ! is_array( $raw ) ) {
			return array();
		}

		$order = array();
		foreach ( $raw as $parent => $ids ) {
			if ( is_array( $ids ) ) {
				$order[ absint( $parent ) ] = array_values( array_unique( array_map( 'absint', $ids ) ) );
			}
		}
		return $order;
	}

	/**
	 * Save the order of one parent's child sections for a user.
	 *
	 * @param int        $user_id   User ID.
	 * @param int        $parent_id Parent term ID (0 for top-level sections).
	 * @param array<int> $ids       Child term IDs in display order.
	 * @return array<int, array<int, int>> Updated order.
	 */
	public static function set( int $user_id, int $parent_id, array $ids ): array {
		$order               = self::get( $user_id );
		$order[ $parent_id ] = array_values( array_unique( array_map( 'absint', $ids ) ) );

		update_user_meta( $user_id, self::META_KEY, $order );

		return $order;
	}

	/**
	 * Forget a user's saved section order so the default order applies again.
	 *
	 * @param int $user_id User ID.
	 * @return void
	 */
	public static function clear( int $user_id ): void {
		delete_user_meta( $user_id, self::META_KEY );
	}
}
