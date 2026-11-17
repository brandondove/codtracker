/**
 * Editor registration: previews the server-rendered checklist.
 */
( function ( wp ) {
	const { registerBlockType } = wp.blocks;
	const { createElement: el } = wp.element;
	const { useBlockProps } = wp.blockEditor;
	const ServerSideRender = wp.serverSideRender;

	registerBlockType( 'codt/checklist', {
		edit() {
			return el(
				'div',
				useBlockProps(),
				el( ServerSideRender, { block: 'codt/checklist' } )
			);
		},
		save() {
			return null;
		},
	} );
} )( window.wp );
