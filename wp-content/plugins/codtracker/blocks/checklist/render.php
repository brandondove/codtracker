<?php
/**
 * Server render for the codt/checklist block.
 *
 * @package CodTracker
 *
 * @var array    $attributes Block attributes.
 * @var string   $content    Inner content.
 * @var WP_Block $block      Block instance.
 */

declare( strict_types = 1 );

defined( 'ABSPATH' ) || exit;

$codt_tree      = CodTracker_Content::get_tree();
$codt_logged_in = is_user_logged_in();
$codt_progress  = $codt_logged_in ? CodTracker_Progress::get( get_current_user_id() ) : array();

if ( ! function_exists( 'codt_render_item' ) ) {
	/**
	 * Render one checklist item.
	 *
	 * @param WP_Post         $item      Item post.
	 * @param array<int, int> $progress  Item ID => completion count.
	 * @param bool            $logged_in Whether the viewer can save.
	 * @return void
	 */
	function codt_render_item( WP_Post $item, array $progress, bool $logged_in ): void {
		$goal         = CodTracker_Progress::goal( $item->ID );
		$count        = min( $progress[ $item->ID ] ?? 0, $goal );
		$is_collected = $count >= $goal;
		$confirmed    = (bool) get_post_meta( $item->ID, 'codt_confirmed', true );
		$details      = array(
			__( 'How to unlock', 'codtracker' ) => (string) get_post_meta( $item->ID, 'codt_requirement', true ),
			__( 'Reward', 'codtracker' )        => (string) get_post_meta( $item->ID, 'codt_reward', true ),
			__( 'Location', 'codtracker' )      => (string) get_post_meta( $item->ID, 'codt_location', true ),
		);
		$details      = array_filter( $details );
		$sources      = array_values( array_filter( array_map( 'trim', explode( "\n", (string) get_post_meta( $item->ID, 'codt_sources', true ) ) ) ) );
		$search       = strtolower( wp_strip_all_tags( $item->post_title . ' ' . $item->post_content . ' ' . implode( ' ', $details ) ) );
		$input_id     = 'codt-item-' . $item->ID;
		?>
		<li class="codt-item<?php echo $is_collected ? ' is-collected' : ''; ?>" data-id="<?php echo esc_attr( (string) $item->ID ); ?>" data-goal="<?php echo esc_attr( (string) $goal ); ?>" data-count="<?php echo esc_attr( (string) $count ); ?>" data-confirmed="<?php echo $confirmed ? '1' : '0'; ?>" data-search="<?php echo esc_attr( $search ); ?>">
			<div class="codt-item__row">
				<?php if ( $goal > 1 ) : ?>
					<span class="codt-counter" role="group" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: item title. */ __( 'Progress for %s', 'codtracker' ), $item->post_title ) ); ?>">
						<button type="button" class="codt-counter__btn" data-step="-1" aria-label="<?php esc_attr_e( 'Decrease', 'codtracker' ); ?>" <?php disabled( ! $logged_in || 0 === $count ); ?>>&minus;</button>
						<span class="codt-counter__value" aria-live="polite"><?php echo esc_html( $count . ' / ' . $goal ); ?></span>
						<button type="button" class="codt-counter__btn" data-step="1" aria-label="<?php esc_attr_e( 'Increase', 'codtracker' ); ?>" <?php disabled( ! $logged_in || $is_collected ); ?>>+</button>
					</span>
					<span class="codt-item__title"><?php echo esc_html( $item->post_title ); ?></span>
					<span class="codt-bar codt-item__bar" aria-hidden="true"><span class="codt-bar__fill" style="width: <?php echo esc_attr( number_format( ( $count / $goal ) * 100, 1, '.', '' ) ); ?>%"></span></span>
				<?php else : ?>
					<input type="checkbox" class="codt-item__check" id="<?php echo esc_attr( $input_id ); ?>" <?php checked( $is_collected ); ?> <?php disabled( ! $logged_in ); ?> />
					<label class="codt-item__title" for="<?php echo esc_attr( $input_id ); ?>"><?php echo esc_html( $item->post_title ); ?></label>
				<?php endif; ?>
				<?php if ( ! $confirmed ) : ?>
					<span class="codt-badge" title="<?php esc_attr_e( 'Reported by a single or unofficial source. Details may change.', 'codtracker' ); ?>"><?php esc_html_e( 'Unconfirmed', 'codtracker' ); ?></span>
				<?php endif; ?>
			</div>
			<?php if ( $details || $item->post_content || $sources ) : ?>
				<details class="codt-item__more">
					<summary><?php esc_html_e( 'Details', 'codtracker' ); ?></summary>
					<?php if ( $item->post_content ) : ?>
						<p><?php echo esc_html( $item->post_content ); ?></p>
					<?php endif; ?>
					<?php if ( $details ) : ?>
						<dl>
							<?php foreach ( $details as $label => $value ) : ?>
								<dt><?php echo esc_html( $label ); ?></dt>
								<dd><?php echo esc_html( $value ); ?></dd>
							<?php endforeach; ?>
						</dl>
					<?php endif; ?>
					<?php if ( $sources ) : ?>
						<p class="codt-item__sources">
							<?php esc_html_e( 'Sources:', 'codtracker' ); ?>
							<?php foreach ( $sources as $codt_i => $url ) : ?>
								<a href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener noreferrer"><?php echo esc_html( (string) wp_parse_url( $url, PHP_URL_HOST ) ); ?></a><?php echo $codt_i < count( $sources ) - 1 ? ', ' : ''; ?>
							<?php endforeach; ?>
						</p>
					<?php endif; ?>
				</details>
			<?php endif; ?>
		</li>
		<?php
	}
}

if ( ! function_exists( 'codt_render_category' ) ) {
	/**
	 * Render a category section and its descendants.
	 *
	 * @param array<string, mixed> $node      Category node from CodTracker_Content::get_tree().
	 * @param array<int, int>      $progress  Item ID => completion count.
	 * @param bool                 $logged_in Whether the viewer can save.
	 * @param int                  $depth     Nesting depth (0 = top level).
	 * @return void
	 */
	function codt_render_category( array $node, array $progress, bool $logged_in, int $depth = 0 ): void {
		$term = $node['term'];
		$tag  = 0 === $depth ? 'h2' : 'h3';
		?>
		<section class="codt-cat codt-cat--depth-<?php echo esc_attr( (string) min( $depth, 2 ) ); ?>" data-cat="<?php echo esc_attr( $term->slug ); ?>">
			<details>
				<summary class="codt-cat__head">
					<<?php echo esc_html( $tag ); ?> class="codt-cat__title"><?php echo esc_html( $term->name ); ?></<?php echo esc_html( $tag ); ?>>
					<span class="codt-cat__count" aria-live="polite"></span>
					<span class="codt-bar" aria-hidden="true"><span class="codt-bar__fill"></span></span>
					<?php if ( $logged_in && $node['items'] ) : ?>
						<button type="button" class="codt-cat__bulk"><?php esc_html_e( 'Mark completed', 'codtracker' ); ?></button>
					<?php endif; ?>
					<button type="button" class="codt-cat__pin" aria-pressed="false" aria-label="<?php echo esc_attr( sprintf( /* translators: %s: section name. */ __( 'Pin to wheel: %s', 'codtracker' ), $term->name ) ); ?>">
						<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false"><path d="M9 3h6l-1 6 4 4v2h-5v6l-1 1-1-1v-6H6v-2l4-4z" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/></svg>
					</button>
				</summary>
				<?php if ( $term->description ) : ?>
					<p class="codt-cat__desc"><?php echo esc_html( $term->description ); ?></p>
				<?php endif; ?>
				<?php if ( $node['items'] ) : ?>
					<ul class="codt-items">
						<?php
						foreach ( $node['items'] as $item ) {
							codt_render_item( $item, $progress, $logged_in );
						}
						?>
					</ul>
				<?php endif; ?>
				<?php
				foreach ( $node['children'] as $child ) {
					codt_render_category( $child, $progress, $logged_in, $depth + 1 );
				}
				?>
			</details>
		</section>
		<?php
	}
}

$codt_wrapper = get_block_wrapper_attributes(
	array(
		'class'          => 'codt-tracker',
		'data-endpoint'  => esc_url_raw( rest_url( CodTracker_Rest::NAMESPACE . '/progress' ) ),
		'data-bulk'      => esc_url_raw( rest_url( CodTracker_Rest::NAMESPACE . '/progress/bulk' ) ),
		'data-nonce'     => $codt_logged_in ? wp_create_nonce( 'wp_rest' ) : '',
		'data-logged-in' => $codt_logged_in ? '1' : '0',
	)
);
?>
<div <?php echo $codt_wrapper; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- Escaped by get_block_wrapper_attributes(). ?>>
	<?php if ( ! $codt_tree ) : ?>
		<p><?php esc_html_e( 'No checklist items yet. Run `wp codt seed` or add items under DMZ Tracker in wp-admin.', 'codtracker' ); ?></p>
	<?php else : ?>
		<?php if ( ! $codt_logged_in ) : ?>
			<p class="codt-notice">
				<?php
				printf(
					/* translators: %s: login URL. */
					wp_kses( __( '<a href="%s">Log in</a> to track your progress.', 'codtracker' ), array( 'a' => array( 'href' => array() ) ) ),
					esc_url( wp_login_url( get_permalink() ? (string) get_permalink() : home_url() ) )
				);
				?>
			</p>
		<?php endif; ?>

		<div class="codt-summary">
			<div class="codt-summary__text"><strong class="codt-summary__count"></strong> <?php esc_html_e( 'collected', 'codtracker' ); ?></div>
			<span class="codt-bar codt-bar--lg" aria-hidden="true"><span class="codt-bar__fill"></span></span>
		</div>

		<div class="codt-toolbar" role="search">
			<label class="screen-reader-text" for="codt-search"><?php esc_html_e( 'Search checklist', 'codtracker' ); ?></label>
			<input type="search" id="codt-search" class="codt-toolbar__search" placeholder="<?php esc_attr_e( 'Search items, rewards, locations…', 'codtracker' ); ?>" />
			<div class="codt-toolbar__filters" role="group" aria-label="<?php esc_attr_e( 'Filter', 'codtracker' ); ?>">
				<button type="button" class="codt-filter is-active" data-filter="all" aria-pressed="true"><?php esc_html_e( 'All', 'codtracker' ); ?></button>
				<button type="button" class="codt-filter" data-filter="missing" aria-pressed="false"><?php esc_html_e( 'Still need', 'codtracker' ); ?></button>
				<button type="button" class="codt-filter" data-filter="collected" aria-pressed="false"><?php esc_html_e( 'Collected', 'codtracker' ); ?></button>
			</div>
			<label class="codt-toolbar__toggle"><input type="checkbox" class="codt-toggle-unconfirmed" checked /> <?php esc_html_e( 'Show unconfirmed', 'codtracker' ); ?></label>
			<button type="button" class="codt-expand" data-expanded="0"><?php esc_html_e( 'Expand all', 'codtracker' ); ?></button>
			<button type="button" class="codt-wheel-btn" aria-expanded="false" aria-controls="codt-wheel-panel"><?php esc_html_e( 'Ping wheel', 'codtracker' ); ?> <span class="codt-wheel-btn__count"></span></button>
			<div class="codt-wheel-panel" id="codt-wheel-panel" hidden>
				<p class="codt-wheel-panel__hint">
					<?php
					printf(
						/* translators: %s: keyboard key name. */
						esc_html__( 'Hold %s, point at a section, and release to jump to it. Pin up to 8 sections with the pin on each section header, then set their order here.', 'codtracker' ),
						'<kbd>' . esc_html__( 'Left Ctrl', 'codtracker' ) . '</kbd>'
					);
					?>
				</p>
				<p class="codt-wheel-panel__empty"><?php esc_html_e( 'Nothing pinned yet.', 'codtracker' ); ?></p>
				<ol class="codt-wheel-panel__list"></ol>
			</div>
		</div>

		<div class="codt-status" role="status" aria-live="polite"></div>

		<?php
		foreach ( $codt_tree as $codt_node ) {
			codt_render_category( $codt_node, $codt_progress, $codt_logged_in );
		}
		?>
		<p class="codt-empty" hidden><?php esc_html_e( 'Nothing matches those filters.', 'codtracker' ); ?></p>
	<?php endif; ?>
</div>
