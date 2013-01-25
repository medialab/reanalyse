var oo = oo || {}; oo.vars.sidebar = oo.vars.sidebar || {};

oo.sidebar = {  is_hidden:false, element:[] };
oo.sidebar.init = function(){
	oo.sidebar.is_hidden = false;
	oo.sidebar.element = $("sidebar");
	$("#collapse-menu").click( oo.sidebar.collapse );
	$("#expand-menu").click( oo.sidebar.expand );

	$("#right-sidebar").height($(".page").first().height());
}

oo.sidebar.collapse = function(){
	oo.sidebar.element.addClass("collapsed");
	$("#collapse-menu").hide();
	$("#expand-menu").show();
}

oo.sidebar.expand = function(){
	oo.sidebar.element.removeClass("collapsed");
	$("#collapse-menu").show();
	$("#expand-menu").hide();
}

