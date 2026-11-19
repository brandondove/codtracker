<?php
/**
 * Per-user progress storage.
 *
 * @package CodTracker
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

/**
 * Stores per-item progress counts for each user in user meta, as item_id => count.
 * Simple checklist items use a count of 1; counter items (e.g. weapon manuals) go up to their goal.
 */
class CodTracker_Progress {

	public const META_KEY = 'codt_progress';

	/**
	 * Get progress counts for a user.
	 *
	 * @param int $user_id User ID.
	 * @return array<int, int> Item ID => count. Items with no progress are omitted.
	 */
	public static function get( int $user_id ): array {
		$raw = get_user_meta( $user_id, self::META_KEY, true );
		if ( ! is_array( $raw ) ) {
			return array();
		}

		// Older format stored a plain list of collected IDs; treat each as count 1.
		if ( array_is_list( $raw ) ) {
			return array_fill_keys( array_map( 'absint', $raw ), 1 );
		}

		$counts = array();
		foreach ( $raw as $item_id => $count ) {
			$count = absint( $count );
			if ( $count > 0 ) {
				$counts[ absint( $item_id ) ] = $count;
			}
		}
		return $counts;
	}

	/**
	 * Set an item's progress count for a user, clamped to 0..goal.
	 *
	 * @param int $user_id User ID.
	 * @param int $item_id Checklist item post ID.
	 * @param int $count   New count.
	 * @return array<int, int> Updated counts.
	 */
	public static function set( int $user_id, int $item_id, int $count ): array {
		$counts = self::get( $user_id );
		$count  = max( 0, min( $count, self::goal( $item_id ) ) );

		if ( $count > 0 ) {
			$counts[ $item_id ] = $count;
		} else {
			unset( $counts[ $item_id ] );
		}

		update_user_meta( $user_id, self::META_KEY, $counts );

		return $counts;
	}

	/**
	 * Mark several items collected (count = goal) or cleared (count = 0) in one write.
	 *
	 * @param int        $user_id   User ID.
	 * @param array<int> $item_ids  Checklist item post IDs.
	 * @param bool       $collected True to fill each item to its goal, false to clear it.
	 * @return array<int, int> Updated counts.
	 */
	public static function set_many( int $user_id, array $item_ids, bool $collected ): array {
		$counts = self::get( $user_id );

		foreach ( $item_ids as $item_id ) {
			$item_id = absint( $item_id );
			if ( $collected ) {
				$counts[ $item_id ] = self::goal( $item_id );
			} else {
				unset( $counts[ $item_id ] );
			}
		}

		update_user_meta( $user_id, self::META_KEY, $counts );

		return $counts;
	}

	/**
	 * How many completions an item needs (1 for a plain checkbox).
	 *
	 * @param int $item_id Checklist item post ID.
	 * @return int
	 */
	public static function goal( int $item_id ): int {
		return max( 1, (int) get_post_meta( $item_id, 'codt_goal', true ) );
	}
}
