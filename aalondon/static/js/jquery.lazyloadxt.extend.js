jQuery.lazyLoadXT.updateEvent = 'load orientationchange resize scroll touchmove focus click customlazyloadxtevent';
jQuery.lazyLoadXT.edgeY = a3_lazyload_extend_params.edgeY;
jQuery.lazyLoadXT.srcsetExtended = false;

jQuery( document ).ready( function( $ ) {
	jQuery(document).on( 'mouseenter', '.site-header-cart', function() {
		jQuery(document).trigger('customlazyloadxtevent');
	});
	jQuery(document).on( 'mouseenter', '.widget_shopping_cart', function() {
		jQuery(document).trigger('customlazyloadxtevent');
	});
	jQuery(document).on( 'mouseover', '#wp-admin-bar-top-secondary', function() {
		jQuery(document).trigger('customlazyloadxtevent');
	});
});

jQuery(window).on('ajaxComplete', function() {
    setTimeout(function() {
        jQuery(window).lazyLoadXT();
    }, 1000 );
});