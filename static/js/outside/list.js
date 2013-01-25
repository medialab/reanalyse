oo.list = {};

oo.list.init = function(){ oo.log("[oo.list.init]");
	$('.items-container').width(650).masonry({ itemSelector : '.item' });
	oo.sidebar.init();
}