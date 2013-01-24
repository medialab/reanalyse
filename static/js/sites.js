oo.sites = {}

oo.sites.init = function(){
	$('li.site').popover({'trigger':'hover'});//.first().popover('show');
	$('.link').popover({'trigger':'hover','placement':'bottom'});
}