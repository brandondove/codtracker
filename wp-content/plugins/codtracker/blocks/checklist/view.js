/**
 * Front-end behaviour for the DMZ checklist: saving, counts, search, and filters.
 */
( function () {
	'use strict';

	function init( root ) {
		const endpoint = root.dataset.endpoint;
		const nonce = root.dataset.nonce;
		const status = root.querySelector( '.codt-status' );
		const search = root.querySelector( '.codt-toolbar__search' );
		const showUnconfirmed = root.querySelector( '.codt-toggle-unconfirmed' );
		const expandBtn = root.querySelector( '.codt-expand' );
		const empty = root.querySelector( '.codt-empty' );
		let filter = 'all';
		const storageKey = 'codt-open-sections';

		// Read the saved list of open category slugs; storage can be unavailable or hold junk.
		function readOpen() {
			try {
				const saved = JSON.parse( window.localStorage.getItem( storageKey ) || '[]' );
				return Array.isArray( saved ) ? saved : [];
			} catch ( e ) {
				return [];
			}
		}

		function writeOpen( slugs ) {
			try {
				window.localStorage.setItem( storageKey, JSON.stringify( slugs ) );
			} catch ( e ) {
				// Storage full or blocked; the open state just won't persist.
			}
		}

		function setBar( bar, done, total ) {
			const fill = bar && bar.querySelector( '.codt-bar__fill' );
			if ( fill ) {
				fill.style.width = total ? ( ( done / total ) * 100 ).toFixed( 1 ) + '%' : '0%';
			}
		}

		function updateCounts() {
			root.querySelectorAll( '.codt-cat' ).forEach( ( cat ) => {
				const items = cat.querySelectorAll( '.codt-item' );
				const done = cat.querySelectorAll( '.codt-item.is-collected' ).length;
				const head = cat.querySelector( ':scope > details > .codt-cat__head' );
				head.querySelector( '.codt-cat__count' ).textContent = done + ' / ' + items.length;
				setBar( head.querySelector( '.codt-bar' ), done, items.length );
				cat.classList.toggle( 'is-complete', items.length > 0 && done === items.length );
			} );
			const all = root.querySelectorAll( '.codt-item' ).length;
			const done = root.querySelectorAll( '.codt-item.is-collected' ).length;
			root.querySelector( '.codt-summary__count' ).textContent =
				done + ' / ' + all + ' (' + ( all ? Math.round( ( done / all ) * 100 ) : 0 ) + '%)';
			setBar( root.querySelector( '.codt-summary .codt-bar' ), done, all );
		}

		function applyFilters() {
			const q = search.value.trim().toLowerCase();
			const filtering = q !== '' || filter !== 'all';
			let anyVisible = false;

			root.querySelectorAll( '.codt-item' ).forEach( ( item ) => {
				const collected = item.classList.contains( 'is-collected' );
				let visible = true;
				if ( filter === 'missing' && collected ) visible = false;
				if ( filter === 'collected' && ! collected ) visible = false;
				if ( ! showUnconfirmed.checked && item.dataset.confirmed === '0' ) visible = false;
				if ( q && item.dataset.search.indexOf( q ) === -1 ) visible = false;
				item.hidden = ! visible;
				anyVisible = anyVisible || visible;
			} );

			// Hide sections with no visible items; open everything while filtering so matches show.
			Array.from( root.querySelectorAll( '.codt-cat' ) ).reverse().forEach( ( cat ) => {
				const hasVisible = !! cat.querySelector( '.codt-item:not([hidden])' );
				cat.hidden = ! hasVisible;
				if ( filtering && hasVisible ) {
					cat.querySelector( ':scope > details' ).open = true;
				}
			} );

			empty.hidden = anyVisible;
		}

		function announce( msg ) {
			status.textContent = msg;
		}

		// Reflect a count in the item's classes, checkbox, and counter controls.
		function setItem( item, count ) {
			const goal = Number( item.dataset.goal ) || 1;
			item.dataset.count = String( count );
			item.classList.toggle( 'is-collected', count >= goal );
			item.classList.toggle( 'is-partial', count > 0 && count < goal );
			const box = item.querySelector( '.codt-item__check' );
			if ( box ) {
				box.checked = count >= goal;
			}
			const value = item.querySelector( '.codt-counter__value' );
			if ( value ) {
				value.textContent = count + ' / ' + goal;
				item.querySelector( '[data-step="-1"]' ).disabled = count <= 0;
				item.querySelector( '[data-step="1"]' ).disabled = count >= goal;
			}
		}

		function setBusy( item, busy ) {
			item.classList.toggle( 'is-saving', busy );
			item.querySelectorAll( '.codt-item__check, .codt-counter__btn' ).forEach( ( el ) => {
				if ( busy ) {
					el.disabled = true;
				}
			} );
		}

		// Optimistically update, save, and roll back on failure.
		function save( item, count ) {
			const previous = Number( item.dataset.count ) || 0;
			setItem( item, count );
			updateCounts();
			setBusy( item, true );

			window
				.fetch( endpoint, {
					method: 'POST',
					credentials: 'same-origin',
					headers: { 'Content-Type': 'application/json', 'X-WP-Nonce': nonce },
					body: JSON.stringify( { item_id: Number( item.dataset.id ), count } ),
				} )
				.then( ( res ) => {
					if ( ! res.ok ) {
						throw new Error( res.status );
					}
					announce( '' );
				} )
				.catch( () => {
					count = previous;
					announce( 'Could not save. Check your connection or log in again.' );
				} )
				.finally( () => {
					setBusy( item, false );
					const box = item.querySelector( '.codt-item__check' );
					if ( box ) {
						box.disabled = false;
					}
					setItem( item, count );
					updateCounts();
					applyFilters();
				} );
		}

		root.addEventListener( 'change', ( event ) => {
			const box = event.target;
			if ( ! box.classList.contains( 'codt-item__check' ) ) {
				return;
			}
			const item = box.closest( '.codt-item' );
			save( item, box.checked ? Number( item.dataset.goal ) || 1 : 0 );
		} );

		root.addEventListener( 'click', ( event ) => {
			const btn = event.target.closest( '.codt-counter__btn' );
			if ( ! btn || btn.disabled ) {
				return;
			}
			const item = btn.closest( '.codt-item' );
			const goal = Number( item.dataset.goal ) || 1;
			const next = Math.max( 0, Math.min( goal, ( Number( item.dataset.count ) || 0 ) + Number( btn.dataset.step ) ) );
			save( item, next );
		} );

		search.addEventListener( 'input', applyFilters );
		showUnconfirmed.addEventListener( 'change', applyFilters );

		root.querySelectorAll( '.codt-filter' ).forEach( ( btn ) => {
			btn.addEventListener( 'click', () => {
				filter = btn.dataset.filter;
				root.querySelectorAll( '.codt-filter' ).forEach( ( b ) => {
					b.classList.toggle( 'is-active', b === btn );
					b.setAttribute( 'aria-pressed', b === btn ? 'true' : 'false' );
				} );
				applyFilters();
			} );
		} );

		// Remember sections the user opens or closes by hand. Expand all and search/filter
		// auto-open change the view only, not the saved state.
		root.addEventListener( 'click', ( event ) => {
			const head = event.target.closest( '.codt-cat__head' );
			if ( ! head ) {
				return;
			}
			const slug = head.closest( '.codt-cat' ).dataset.cat;
			const willOpen = ! head.parentElement.open;
			const saved = readOpen().filter( ( s ) => s !== slug );
			if ( willOpen ) {
				saved.push( slug );
			}
			writeOpen( saved );
		} );

		expandBtn.addEventListener( 'click', () => {
			const expand = expandBtn.dataset.expanded !== '1';
			root.querySelectorAll( '.codt-cat > details' ).forEach( ( d ) => ( d.open = expand ) );
			expandBtn.dataset.expanded = expand ? '1' : '0';
			expandBtn.textContent = expand ? 'Collapse all' : 'Expand all';
		} );

		readOpen().forEach( ( slug ) => {
			const details = root.querySelector( '.codt-cat[data-cat="' + CSS.escape( slug ) + '"] > details' );
			if ( details ) {
				details.open = true;
			}
		} );

		root.querySelectorAll( '.codt-item' ).forEach( ( item ) => {
			item.classList.toggle( 'is-partial', ( Number( item.dataset.count ) || 0 ) > 0 && ! item.classList.contains( 'is-collected' ) );
		} );
		updateCounts();
	}

	function boot() {
		document.querySelectorAll( '.codt-tracker[data-endpoint]' ).forEach( init );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', boot );
	} else {
		boot();
	}
} )();
