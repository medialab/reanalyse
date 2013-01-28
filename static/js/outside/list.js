oo.list = {};

oo.list.init = function(){ oo.log("[oo.list.init]");

	$('.items-container').masonry({ itemSelector : '.item' });
	oo.sidebar.init();
}