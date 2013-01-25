var oo = oo || {}; oo.vars.pin = oo.vars.pin || {}; oo.glue = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.reload = function(){
	window.location.reload();
}

oo.magic.page = oo.magic.page || {};

oo.magic.page.add = function( result ){
	oo.log("[oo.magic.page.add]", result);
	window.location.reload();
}

oo.magic.pin = oo.magic.pin || {};
oo.magic.pin.add = function( result ){
	oo.log("[oo.magic.pin.add]", result);
	window.location.reload();
}
oo.magic.pin.get = function( result ){
	oo.log("[oo.magic.pin.get]", result);
	// window.location.reload();
}



/*


    Pin/Page Ajax API
    =================

*/
oo.api.pin = {};
oo.api.pin.add = function( params ){
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_pin,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.pin.add] result:", result );
			oo.api.process( result, oo.magic.pin.add, "id_add_pin" );
		}
	}));
};

oo.api.pin.get = function( pk, params, callback ){
	$.ajax( $.extend( oo.api.settings.get,{
		url: oo.api.urlfactory( oo.urls.get_pin, pk ),
		data: params, 
		success:function(result){
			oo.log( "[oo.api.pin.get] result:", result );
			oo.api.process( result, typeof callback == "function"? callback: oo.magic.pin.get );
		}
	}));
};

oo.api.pin.edit = function( pk, params, callback ){
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.api.urlfactory( oo.urls.edit_pin, pk ),
		data: params, 
		success:function(result){
			oo.log( "[oo.api.pin.edit] result:", result );
			oo.api.process( result, typeof callback == "function"? callback: oo.magic.reload,"id_edit_pin" );
		}
	}));
};

oo.api.pin.delete = function( pk, params, callback ){
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.api.urlfactory( oo.urls.edit_pin, pk ),
		data: $.extend({'method':'DELETE'}, params),
		success:function(result){
			oo.log( "[oo.api.pin.delete] deleted : "+ pk);
			oo.api.process( result, typeof callback == "function"? callback: oo.magic.reload);
		}
	}));
};

oo.api.pin.publish = function( pk, params, callback ){
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.api.urlfactory( oo.urls.publish_pin, pk ),
		data:  params,
		success:function(result){
			//oo.log( "[oo.api.pin.publish] pin #"+ pk+"new status is : "+params.new_status);
			oo.api.process( result, typeof callback == "function"? callback: oo.magic.reload);
		}
	}));
};


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
    =============

	Require wysihtml5 plugin

*/
oo.glue = {};
oo.glue.init = function(){ oo.log("[oo.glue.init]");
	$("#add-page").on("click", function(event){ event.preventDefault(); oo.api.page.add({
		title_en:$("#id_add_page_title_en").val(),
		title_fr:$("#id_add_page_title_fr").val(),
		slug:$("#id_add_page_slug").val()
	});});

	$("#add-pin").on("click", function(event){ event.preventDefault(); 
		var el = $(this);
		oo.log("[oo.glue.init:click] #add-pin, page-slug:", el.attr("data-page-slug"), ", parent-pin-slug:", el.attr("data-parent-pin-slug") );

		var params = {
			title_en:$("#id_add_pin_title_en").val(),
			title_fr:$("#id_add_pin_title_fr").val(),
			slug:$("#id_add_pin_slug").val()
		}
		if ( typeof el.attr("data-page-slug") != "undefined" ){
			$.extend(params,{page_slug:el.attr("data-page-slug")});
		}

		if ( typeof el.attr("data-parent-pin-slug") != "undefined" ){
			$.extend(params,{parent_pin_slug:el.attr("data-parent-pin-slug")});
		}
		oo.api.pin.add( params );
	});
		

	$("#edit-pin").on("click", function(event){ event.preventDefault(); oo.api.pin.edit( $(this).attr("data-pin-id"),{
		title:$("#id_edit_pin_title").val(),
		content:$("#id_edit_pin_content").val(),
		abstract:$("#id_edit_pin_abstract").val()
	});});

	$("#id_add_page_title_en").on('keyup', function( event ){ $("#id_add_page_slug").val( oo.fn.slug( $("#id_add_page_title_en").val() ) ) });
	$("#id_add_pin_title_en").on('keyup', function( event ){ $("#id_add_pin_slug").val( oo.fn.slug( $("#id_add_pin_title_en").val() ) ) });



	// html5 pin editor
	try{
		var editor = new wysihtml5.Editor("id_edit_pin_content", { // id of textarea element
			toolbar:      "wysihtml5-toolbar", // id of toolbar element
			parserRules:  wysihtml5ParserRules // defined in parser rules set 
		});
	} catch(e){
		oo.log("[oo.glue.init:exception]",e);
	}
	// $("#edit-section-modal").modal('show')
	$(document).click( function(event){ $(".invalid").removeClass('invalid');});

	// ADD PIN
	$(document).on("click",".add-pin", function(event){
		var el = $(this);
		oo.log("[oo.glue.init:click] .add-pin", el.attr("data-page-slug"),  el.attr('data-parent-pin-slug') );
		$('#add-pin-modal').modal('show');
		
		if( typeof el.attr('data-parent-pin-slug') == "undefined"){
			$('#parent-pin-slug').empty();
		} else {
			$('#parent-pin-slug').html( "&rarr;" + el.attr('data-parent-pin-slug') )
		}

		if( typeof el.attr('data-page-slug') == "undefined"){
			$('#parent-page-slug').empty();	// news!
		} else {
			$('#parent-page-slug').html( "&rarr;" + el.attr('data-parent-slug') )
		}

		$('#add-pin').attr("data-parent-pin-slug", el.attr('data-parent-pin-slug') );
		$('#add-pin').attr("data-page-slug", el.attr('data-page-slug') );

	});

	$(document).on("click",".edit-pin", function(event){ 
		// load content before all
		oo.api.pin.get( $(this).attr('data-pin-id'), {}, function(result){
			$('#edit-pin-modal').modal('show');
			$('#id_edit_pin_title').val( result.object.title )
			$('#id_edit_pin_abstract').val( result.object.abstract )
			$('#id_edit_pin_content').val( result.object.content )
			editor.setValue( result.object.content );
			// $('#edit-pin-modal').result.object.title
			$('#edit-pin').attr("data-pin-id",result.object.id );
		});
		oo.log("eeee");
	});
	
	// Delete PIN
	$(document).on("click",".delete-pin", function(event){
		oo.api.pin.delete($(this).attr('data-pin-id'),{});
	});
	
	//Publish PIN
	$(document).on("click",".publish-pin", function(event){
		oo.api.pin.publish($(this).attr('data-pin-id'),{'new_status':$(this).attr('new-status')});
	});
	
};


oo.glue.upload = { is_dragging:false }
oo.glue.upload.enable = function()
{
	oo.log("[oo.glue.upload.enable]");
	$('#fileupload').fileupload('enable');
}

oo.glue.upload.disable = function(){
	oo.log("[oo.glue.upload.disable]");
	$('#fileupload').fileupload('disable');
}
oo.glue.upload.init = function(){
	oo.log("[oo.glue.init]");

	$('#fileupload').fileupload({
		url: oo.urls.pin_upload,
		dataType: 'json',
		sequentialUploads: true,
		dragover: function(e,data){
			if (oo.glue.upload.is_dragging)
				return;
			oo.log("[oo.glue.upload] dragover");
			oo.glue.upload.is_dragging = true;
		},
		drop:function(e,data){
			oo.log("[oo.glue.upload] drop");
			oo.glue.upload.is_dragging = false;
		},
		done: function (e, data) {
			oo.log( e, data.result);
			oo.toast("uploaded finished", { stayTime: 2000,cleanup:true });
			if( data.result.status == "ok"){
				oo.toast( "COMPLETED GUY!:!!!" );
			} else{
				oo.toast( data.result.error, ds.i18n.translate("error"), { stayTime: 2000, cleanup:true });	
			}
		},
		start: function (e, data) {
			oo.toast(oo.i18n.translate("start uploading"), { stayTime: 2000 });
		},
		fail: function( e, data){
			oo.log(e, data);
			oo.fault( e.type);
		},
		progressall: function (e, data) {
			var progress = parseInt(data.loaded / data.total * 100, 10);
			$('#progress .bar').width( progress + '%');
		},

    	add: function (e, data) {
			var slug = $('body').attr('data-page-slug');
			if( slug.length > 0 ){
				data.formData = { 'page_slug':slug };
			}
			data.submit();
			
		}
	});
	// enabled by default, or comment
	// oo.glue.upload.disable();
};


