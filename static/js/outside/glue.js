var oo = oo || {}; oo.vars.pin = oo.vars.pin || {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.pin = oo.magic.pin || {};
oo.magic.pin.add = function( result ){

}


/*


    Pin Restful API
    ===============

*/
oo.api.pin = {};
oo.api.pin.add = function( param ){
	$.ajax( $.extend( oo.api.settings.get,{
		url: oo.urls.add_pin,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.pin.add] result:", result );
			oo.api.process( result, oo.magic.pin.add );
		}
	}));
}

oo.api.page = {};
oo.api.page.add = function( param ){
	$.ajax( $.extend( oo.api.settings.get,{
		url: oo.urls.add_page,
		data: params, 
		success:function(result){
			ds.log( "[oo.api.page.add] result:", result );
			ds.m.api.process( result, ds.m.magic.survey.get_user_selection );
		}
	}));
}


/*


    Pin Init
    ========

*/
oo.pin = {};
oo.pin.init = function(){

};