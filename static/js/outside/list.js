/*

	List

	This script handle the behaviour of "enquete" item list.
	It make use of masonry to distribute the enquete items through the page


*/
oo.list = {};



oo.list.init = function(){ oo.log("[oo.list.init]");

	$('.items-container').masonry({ itemSelector : '.item' });
	oo.sidebar.init();
	$('.items-container').on('click', ".cover a",function( e ){ e.stopImmediatePropagation(); return true; } );
	$('.items-container').on('click', ".item", oo.list.items.click );
	
	
	// create hidden div
	$('.items-container').on('mouseleave', ".item", oo.list.covers.mouseleave );
}


oo.list.items = {

};

oo.list.items.click = function( event ){
	event.preventDefault();

	$(this).addClass( 'active' );

	return;
}

oo.list.covers = { timeouts:{} };
oo.list.covers.mouseleave = function( event ){
	var id = $(this).attr('data-enquete-id');

	oo.log("oo.list.covers.mouseleave ", id );
	clearTimeout( oo.list.covers.timeouts[  id ] );
	oo.list.covers.timeouts[  id ] = setTimeout( function(){ oo.list.covers.shutdown( id ) }, 500 );
}
oo.list.covers.shutdown = function( id ){
	
	oo.log("[o.list.covers.shutdown]", id);
	$("#cover-of-item-" + id ).parent().removeClass('active');
}
