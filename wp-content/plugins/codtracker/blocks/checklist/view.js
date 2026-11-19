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

		// Sum each item's share of its goal, so 1 of 3 manuals counts as a third of an item.
		function partialDone( items ) {
			let sum = 0;
			items.forEach( ( item ) => {
				const goal = Number( item.dataset.goal ) || 1;
				sum += Math.min( Number( item.dataset.count ) || 0, goal ) / goal;
			} );
			return sum;
		}

		// Items that belong directly to a section, not to its subsections.
		function ownItems( cat ) {
			return Array.from( cat.querySelectorAll( ':scope > details > .codt-items > .codt-item' ) );
		}

		function updateCounts() {
			root.querySelectorAll( '.codt-cat' ).forEach( ( cat ) => {
				const items = cat.querySelectorAll( '.codt-item' );
				const done = cat.querySelectorAll( '.codt-item.is-collected' ).length;
				const head = cat.querySelector( ':scope > details > .codt-cat__head' );
				head.querySelector( '.codt-cat__count' ).textContent = done + ' / ' + items.length;
				setBar( head.querySelector( '.codt-bar' ), partialDone( items ), items.length );
				cat.classList.toggle( 'is-complete', items.length > 0 && done === items.length );

				const bulk = head.querySelector( '.codt-cat__bulk' );
				if ( bulk ) {
					const own = ownItems( cat );
					const label = own.every( ( item ) => item.classList.contains( 'is-collected' ) ) ? 'Mark incomplete' : 'Mark completed';
					bulk.textContent = label;
					bulk.setAttribute( 'aria-label', label + ': ' + head.querySelector( '.codt-cat__title' ).textContent );
				}
			} );
			const allItems = root.querySelectorAll( '.codt-item' );
			const all = allItems.length;
			const done = root.querySelectorAll( '.codt-item.is-collected' ).length;
			const progress = partialDone( allItems );
			root.querySelector( '.codt-summary__count' ).textContent =
				done + ' / ' + all + ' (' + ( all ? Math.round( ( progress / all ) * 100 ) : 0 ) + '%)';
			setBar( root.querySelector( '.codt-summary .codt-bar' ), progress, all );
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
			setBar( item.querySelector( '.codt-item__bar' ), count, goal );
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

		// Fill or clear every item in one section with a single request; roll the batch back on failure.
		function saveMany( items, collected, btn ) {
			const previous = items.map( ( item ) => Number( item.dataset.count ) || 0 );
			let failed = false;

			items.forEach( ( item ) => {
				setItem( item, collected ? Number( item.dataset.goal ) || 1 : 0 );
				setBusy( item, true );
			} );
			btn.disabled = true;
			updateCounts();

			window
				.fetch( root.dataset.bulk, {
					method: 'POST',
					credentials: 'same-origin',
					headers: { 'Content-Type': 'application/json', 'X-WP-Nonce': nonce },
					body: JSON.stringify( { item_ids: items.map( ( item ) => Number( item.dataset.id ) ), collected } ),
				} )
				.then( ( res ) => {
					if ( ! res.ok ) {
						throw new Error( res.status );
					}
					announce( '' );
				} )
				.catch( () => {
					failed = true;
					announce( 'Could not save. Check your connection or log in again.' );
				} )
				.finally( () => {
					items.forEach( ( item, i ) => {
						setBusy( item, false );
						const box = item.querySelector( '.codt-item__check' );
						if ( box ) {
							box.disabled = false;
						}
						setItem( item, failed ? previous[ i ] : Number( item.dataset.count ) || 0 );
					} );
					btn.disabled = false;
					updateCounts();
					applyFilters();
				} );
		}

		root.addEventListener( 'click', ( event ) => {
			const btn = event.target.closest( '.codt-cat__bulk' );
			if ( ! btn ) {
				return;
			}
			// The button sits inside <summary>; don't let the click toggle the section.
			event.preventDefault();
			if ( btn.disabled ) {
				return;
			}
			const items = ownItems( btn.closest( '.codt-cat' ) );
			if ( items.length ) {
				saveMany( items, items.some( ( item ) => ! item.classList.contains( 'is-collected' ) ), btn );
			}
		} );

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
			if ( ! head || event.target.closest( '.codt-cat__bulk, .codt-cat__pin' ) ) {
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

		// Ping wheel: pin up to 8 sections, hold Left Ctrl, release over a slice to jump there.
		const pinKey = 'codt-wheel-pins';
		const maxPins = 8;
		const holdDelay = 150;
		const wheelBtn = root.querySelector( '.codt-wheel-btn' );
		const wheelPanel = root.querySelector( '.codt-wheel-panel' );
		const pinList = wheelPanel.querySelector( '.codt-wheel-panel__list' );
		const reduceMotion = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

		function catBySlug( slug ) {
			return root.querySelector( '.codt-cat[data-cat="' + CSS.escape( slug ) + '"]' );
		}

		function catTitle( cat ) {
			return cat.querySelector( ':scope > details > .codt-cat__head .codt-cat__title' ).textContent;
		}

		// Drop junk and sections that no longer exist.
		function readPins() {
			try {
				const saved = JSON.parse( window.localStorage.getItem( pinKey ) || '[]' );
				return Array.isArray( saved )
					? saved.filter( ( s, i ) => typeof s === 'string' && saved.indexOf( s ) === i && catBySlug( s ) ).slice( 0, maxPins )
					: [];
			} catch ( e ) {
				return [];
			}
		}

		let pins = readPins();

		function setPins( next ) {
			pins = next;
			try {
				window.localStorage.setItem( pinKey, JSON.stringify( pins ) );
			} catch ( e ) {
				// Storage blocked; pins last for this page view only.
			}
			renderPins();
		}

		function pinButton( action, index, text, label, disabled ) {
			const btn = document.createElement( 'button' );
			btn.type = 'button';
			btn.className = 'codt-wheel-panel__btn';
			btn.dataset.action = action;
			btn.dataset.index = String( index );
			btn.textContent = text;
			btn.setAttribute( 'aria-label', label );
			btn.disabled = disabled;
			return btn;
		}

		function renderPins() {
			const full = pins.length >= maxPins;
			root.querySelectorAll( '.codt-cat__pin' ).forEach( ( btn ) => {
				const cat = btn.closest( '.codt-cat' );
				const on = pins.includes( cat.dataset.cat );
				const blocked = ! on && full;
				const label = on ? 'Unpin from wheel' : blocked ? 'Wheel is full (' + maxPins + ' pinned)' : 'Pin to wheel';
				btn.setAttribute( 'aria-pressed', on ? 'true' : 'false' );
				btn.setAttribute( 'aria-disabled', blocked ? 'true' : 'false' );
				btn.setAttribute( 'aria-label', label + ': ' + catTitle( cat ) );
				btn.title = label;
			} );

			wheelBtn.querySelector( '.codt-wheel-btn__count' ).textContent = pins.length + ' / ' + maxPins;
			wheelPanel.querySelector( '.codt-wheel-panel__empty' ).hidden = pins.length > 0;
			pinList.replaceChildren(
				...pins.map( ( slug, i ) => {
					const title = catTitle( catBySlug( slug ) );
					const li = document.createElement( 'li' );
					const name = document.createElement( 'span' );
					name.className = 'codt-wheel-panel__name';
					name.textContent = title;
					li.append(
						name,
						pinButton( 'up', i, '↑', 'Move up: ' + title, i === 0 ),
						pinButton( 'down', i, '↓', 'Move down: ' + title, i === pins.length - 1 ),
						pinButton( 'remove', i, '✕', 'Unpin: ' + title, false )
					);
					return li;
				} )
			);
		}

		root.addEventListener( 'click', ( event ) => {
			const btn = event.target.closest( '.codt-cat__pin' );
			if ( ! btn ) {
				return;
			}
			// The button sits inside <summary>; don't let the click toggle the section.
			event.preventDefault();
			const slug = btn.closest( '.codt-cat' ).dataset.cat;
			if ( pins.includes( slug ) ) {
				setPins( pins.filter( ( s ) => s !== slug ) );
			} else if ( pins.length < maxPins ) {
				setPins( pins.concat( slug ) );
			}
		} );

		wheelBtn.addEventListener( 'click', () => {
			wheelPanel.hidden = ! wheelPanel.hidden;
			wheelBtn.setAttribute( 'aria-expanded', wheelPanel.hidden ? 'false' : 'true' );
		} );

		pinList.addEventListener( 'click', ( event ) => {
			const btn = event.target.closest( '.codt-wheel-panel__btn' );
			if ( ! btn || btn.disabled ) {
				return;
			}
			const i = Number( btn.dataset.index );
			const next = pins.slice();
			if ( btn.dataset.action === 'remove' ) {
				next.splice( i, 1 );
			} else {
				const j = btn.dataset.action === 'up' ? i - 1 : i + 1;
				[ next[ i ], next[ j ] ] = [ next[ j ], next[ i ] ];
			}
			setPins( next );
			// Re-rendering replaces the buttons; keep focus on the same control for keyboard users.
			const again = pinList.querySelector( '[data-action="' + btn.dataset.action + '"][data-index="' + ( btn.dataset.action === 'up' ? i - 1 : btn.dataset.action === 'down' ? i + 1 : i ) + '"]' );
			if ( again && ! again.disabled ) {
				again.focus();
			}
		} );

		// Open the target's ancestors, close every other top-level section, and scroll to it.
		// Subsections inside the target's own tree keep whatever state they had.
		function jumpTo( slug ) {
			const cat = catBySlug( slug );
			if ( ! cat ) {
				return;
			}
			const chain = [];
			for ( let c = cat; c; c = c.parentElement.closest( '.codt-cat' ) ) {
				chain.unshift( c );
			}
			const others = Array.from( root.querySelectorAll( ':scope > .codt-cat' ) ).filter( ( c ) => c !== chain[ 0 ] );
			others.forEach( ( c ) => ( c.querySelector( ':scope > details' ).open = false ) );
			chain.forEach( ( c ) => ( c.querySelector( ':scope > details' ).open = true ) );

			const closed = others.map( ( c ) => c.dataset.cat );
			const opened = chain.map( ( c ) => c.dataset.cat );
			writeOpen( readOpen().filter( ( s ) => ! closed.includes( s ) && ! opened.includes( s ) ).concat( opened ) );

			expandBtn.dataset.expanded = '0';
			expandBtn.textContent = 'Expand all';

			// Land below the sticky toolbar.
			const toolbar = root.querySelector( '.codt-toolbar' );
			const offset = ( parseFloat( window.getComputedStyle( toolbar ).top ) || 0 ) + toolbar.offsetHeight + 8;
			window.scrollTo( {
				top: window.scrollY + cat.getBoundingClientRect().top - offset,
				behavior: reduceMotion ? 'auto' : 'smooth',
			} );
			cat.querySelector( ':scope > details > .codt-cat__head' ).focus( { preventScroll: true } );

			cat.classList.remove( 'is-pinged' );
			void cat.offsetWidth; // Restart the highlight animation on repeat pings.
			cat.classList.add( 'is-pinged' );
		}

		const pointer = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
		let wheel = null;
		let holdTimer = 0;
		let hovered = -1;

		function polar( deg, radius ) {
			const rad = ( deg * Math.PI ) / 180;
			return ( Math.cos( rad ) * radius ).toFixed( 2 ) + ' ' + ( Math.sin( rad ) * radius ).toFixed( 2 );
		}

		// Ring segment from angle a0 to a1 (degrees, clockwise from 3 o'clock).
		function sector( a0, a1, inner, outer ) {
			const large = a1 - a0 > 180 ? 1 : 0;
			return 'M' + polar( a0, outer ) +
				' A' + outer + ' ' + outer + ' 0 ' + large + ' 1 ' + polar( a1, outer ) +
				' L' + polar( a1, inner ) +
				' A' + inner + ' ' + inner + ' 0 ' + large + ' 0 ' + polar( a0, inner ) + 'Z';
		}

		function openWheel() {
			holdTimer = 0;
			// Ring spans about half the screen's shorter side.
			const outer = Math.round( Math.max( 160, Math.min( window.innerWidth, window.innerHeight ) * 0.25 ) );
			const inner = Math.round( outer * 0.36 );
			const labelRadius = outer + 48;
			const size = 2 * ( outer + 150 );
			const count = pins.length;
			const span = count ? 360 / count : 360;
			const gap = count > 1 ? 1.5 : 0;
			const ns = 'http://www.w3.org/2000/svg';

			// Center on the cursor, kept on screen.
			const padX = Math.min( labelRadius + 90, window.innerWidth / 2 );
			const padY = Math.min( labelRadius + 20, window.innerHeight / 2 );
			const cx = Math.min( Math.max( pointer.x, padX ), window.innerWidth - padX );
			const cy = Math.min( Math.max( pointer.y, padY ), window.innerHeight - padY );

			const el = document.createElement( 'div' );
			el.className = 'codt-wheel';
			el.setAttribute( 'aria-hidden', 'true' );
			el.style.left = cx + 'px';
			el.style.top = cy + 'px';
			el.style.width = el.style.height = size + 'px';

			const svg = document.createElementNS( ns, 'svg' );
			svg.setAttribute( 'viewBox', -size / 2 + ' ' + -size / 2 + ' ' + size + ' ' + size );
			svg.setAttribute( 'class', 'codt-wheel__svg' );

			// Gradients that fade from the hub to nothing at the rim: the hover glow,
			// the slice borders, and the slice fill, so the wheel has no hard outer edge.
			const defs = document.createElementNS( ns, 'defs' );
			[
				[ 'codt-wheel-glow', '#f2a313', 0.95 ],
				[ 'codt-wheel-edge', '#e4e4de', 0.35 ],
				[ 'codt-wheel-fill', '#0b0d0e', 0.72 ],
			].forEach( ( [ id, color, start ] ) => {
				const grad = document.createElementNS( ns, 'radialGradient' );
				grad.setAttribute( 'id', id );
				grad.setAttribute( 'gradientUnits', 'userSpaceOnUse' );
				grad.setAttribute( 'cx', '0' );
				grad.setAttribute( 'cy', '0' );
				grad.setAttribute( 'r', String( outer ) );
				[ [ inner / outer, start ], [ 1, 0 ] ].forEach( ( [ offset, opacity ] ) => {
					const stop = document.createElementNS( ns, 'stop' );
					stop.setAttribute( 'offset', String( offset ) );
					stop.setAttribute( 'stop-color', color );
					stop.setAttribute( 'stop-opacity', String( opacity ) );
					grad.append( stop );
				} );
				defs.append( grad );
			} );
			svg.append( defs );
			const ring = document.createElementNS( ns, 'circle' );
			ring.setAttribute( 'r', String( inner - 6 ) );
			ring.setAttribute( 'class', 'codt-wheel__hub' );
			svg.append( ring );

			const labels = [];
			pins.forEach( ( slug, i ) => {
				// Slot 0 is centered at 12 o'clock; the rest go clockwise.
				const a0 = -90 - span / 2 + i * span + gap / 2;
				const a1 = -90 - span / 2 + ( i + 1 ) * span - gap / 2 - ( count === 1 ? 0.01 : 0 );
				const path = document.createElementNS( ns, 'path' );
				path.setAttribute( 'd', sector( a0, a1, inner, outer ) );
				path.setAttribute( 'class', 'codt-wheel__slice' );
				svg.append( path );

				const mid = ( ( -90 + i * span ) * Math.PI ) / 180;
				const label = document.createElement( 'span' );
				label.className = 'codt-wheel__label';
				label.textContent = catTitle( catBySlug( slug ) );
				label.style.left = 'calc(50% + ' + ( Math.cos( mid ) * labelRadius ).toFixed( 1 ) + 'px)';
				label.style.top = 'calc(50% + ' + ( Math.sin( mid ) * labelRadius ).toFixed( 1 ) + 'px)';
				labels.push( label );
			} );

			const center = document.createElement( 'div' );
			center.className = 'codt-wheel__center';
			center.textContent = count ? 'Release to open' : 'Pin sections to fill the wheel';

			el.append( svg, ...labels, center );
			// Full-screen dim + blur; the is-open class on the next frame starts the fade.
			const backdrop = document.createElement( 'div' );
			backdrop.className = 'codt-wheel-backdrop';
			backdrop.setAttribute( 'aria-hidden', 'true' );
			root.append( backdrop, el );
			window.requestAnimationFrame( () => window.requestAnimationFrame( () => backdrop.classList.add( 'is-open' ) ) );
			wheel = { el, backdrop, cx, cy, span, inner, slices: svg.querySelectorAll( '.codt-wheel__slice' ), labels, center };
			hovered = -1;
			track();
		}

		function track() {
			const dx = pointer.x - wheel.cx;
			const dy = pointer.y - wheel.cy;
			let next = -1;
			if ( pins.length && Math.hypot( dx, dy ) >= wheel.inner ) {
				const deg = ( ( Math.atan2( dy, dx ) * 180 ) / Math.PI + 90 + wheel.span / 2 + 720 ) % 360;
				next = Math.min( pins.length - 1, Math.floor( deg / wheel.span ) );
			}
			if ( next === hovered ) {
				return;
			}
			hovered = next;
			wheel.slices.forEach( ( s, i ) => s.classList.toggle( 'is-hovered', i === hovered ) );
			wheel.labels.forEach( ( l, i ) => l.classList.toggle( 'is-hovered', i === hovered ) );
			if ( pins.length ) {
				wheel.center.textContent = hovered < 0 ? 'Release to cancel' : 'Release to open';
			}
		}

		function closeWheel() {
			window.clearTimeout( holdTimer );
			holdTimer = 0;
			if ( wheel ) {
				const backdrop = wheel.backdrop;
				wheel.el.remove();
				wheel = null;
				// Fade the backdrop back out, then drop it.
				backdrop.classList.remove( 'is-open' );
				window.setTimeout( () => backdrop.remove(), reduceMotion ? 0 : 500 );
			}
		}

		document.addEventListener( 'pointermove', ( event ) => {
			pointer.x = event.clientX;
			pointer.y = event.clientY;
			if ( wheel ) {
				track();
			}
		}, { passive: true } );

		// A bare Left Ctrl hold opens the wheel. Any other key or a click cancels, so
		// shortcuts like Ctrl+C and Ctrl+click behave normally.
		document.addEventListener( 'keydown', ( event ) => {
			if ( event.code === 'ControlLeft' && ! event.shiftKey && ! event.altKey && ! event.metaKey ) {
				if ( ! event.repeat && ! wheel && ! holdTimer ) {
					holdTimer = window.setTimeout( openWheel, holdDelay );
				}
				return;
			}
			if ( wheel && event.key === 'Escape' ) {
				event.preventDefault();
			}
			closeWheel();
		} );

		document.addEventListener( 'keyup', ( event ) => {
			if ( event.code !== 'ControlLeft' ) {
				return;
			}
			const pick = wheel && hovered >= 0 ? pins[ hovered ] : null;
			closeWheel();
			if ( pick ) {
				jumpTo( pick );
			}
		} );

		document.addEventListener( 'pointerdown', closeWheel );
		window.addEventListener( 'blur', closeWheel );

		renderPins();

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
