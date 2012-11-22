var oo = oo || {}; oo.vars.pin = oo.vars.pin || {}; oo.glue = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.page = oo.magic.page || {};

oo.magic.page.add = function( result ){
	oo.log("[oo.magic.page.add]", result);
	window.location.reload();
}

oo.magic.pin = oo.magic.pin || {};
oo.magic.pin.add = function( result ){

}




/*


    Pin/Page Ajax API
    =================

*/
oo.api.pin = {};
oo.api.pin.add = function( params ){
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
oo.api.page.add = function( params ){
	oo.log("[oo.api.page.add]");
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_page,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.page.add] result:", result );
			oo.api.process( result, oo.magic.page.add, "id_add_page" );
		}
	}));
}


/*


    Pin/Page Init
    ========

*/
oo.glue = {};
oo.glue.init = function(){ oo.log("[oo.glue.init]");
	$("#add-page").on("click", function(event){ event.preventDefault(); oo.api.page.add({
		title_en:$("#id_add_page_title_en").val(),
		title_fr:$("#id_add_page_title_fr").val(),
		slug:$("#id_add_page_slug").val()
	});});

	$("#id_add_page_title_en").on('keyup', function( event ){ oo.log(event); $("#id_add_page_slug").val( oo.fn.slug( $("#id_add_page_title_en").val() ) ) });

	$(document).click( function(event){ $("form .invalid").removeClass('invalid');});
};
