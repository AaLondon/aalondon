jQuery( document ).ready( function() {
	jQuery( "div[class^='timed-content-client']" ).each( function( index, element ) {
		var clsname = jQuery( this ).attr( "class" );
		var params = clsname.split( "_" );
		for ( var i = 1; i < params.length; i += 4 )  {
			var action = params[i];
			var minutes = parseInt( params[i+1] );
			var seconds = parseInt( params[i+2] );
			var fade = parseInt( params[i+3] );
			var ms = ( ( 60 * minutes ) + seconds ) * 1000;
			if ( ( action == 'show' ) && ( ms > 0 ) )  {
				jQuery( this ).hide( 0 );
				var s = setTimeout( 
						function() {
							jQuery( "div[class='" + clsname + "']" ).show( fade );
						},
						ms );
			}
			if ( ( action == 'hide' ) && ( ms > 0 ) )  {
				var h = setTimeout(
						function() {
							jQuery( "div[class='" + clsname + "']").hide( fade );
						}, ms );
			}
		}
	} );

	jQuery( "span[class^='timed-content-client']" ).each( function( index, element ) {
		var clsname = jQuery( this ).attr( "class" );
		var params = clsname.split( "_" );
		for ( var i = 1; i < params.length; i += 4 )  {
			var action = params[i];
			var minutes = parseInt( params[i+1] );
			var seconds = parseInt( params[i+2] );
			var fade = parseInt( params[i+3] );
			var ms = ( ( 60 * minutes ) + seconds ) * 1000;
			if ( ( action == 'show' ) && ( ms > 0 ) )  {
				jQuery( this ).hide( 0 );
				var s = setTimeout( 
						function() {
							jQuery( "span[class='" + clsname + "']" ).show( fade );
						},
						ms );
			}
			if ( ( action == 'hide' ) && ( ms > 0 ) )  {
				var h = setTimeout(
						function() {
							jQuery( "span[class='" + clsname + "']").hide( fade );
						}, ms );
			}
		}
	} );
} );