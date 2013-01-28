var oo = oo || {}; oo.vars.pin = oo.vars.pin || {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.enquiry = {}

oo.magic.enquiry.add = function( result ){
	oo.log("[oo.magic.enquiry.add]", result);
	window.location.reload();
}

oo.api.enquiry = {};
oo.api.enquiry.add = function( params ){
	oo.log("[oo.api.enquiry.add]");
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_enquiry,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.enquiry.add] result:", result );
			oo.api.process( result, oo.magic.enquiry.add, "id_add_enquiry" );
		}
	}));
}


/*


    Enquiry Init
    ============

	Require wysihtml5 plugin

*/
oo.enquiry = {};
oo.enquiry.init = function(){ oo.log("[oo.enquiry.init]");
	
	$('#add-enquiry-modal').modal({show:false})

	/*
		ADD new enquiry
		---------------
	*/
	$(document).on("click",".add-enquiry", function(event){$('#add-enquiry-modal').modal('show');});
	$("#id_add_enquiry_title_en").on('keyup', function( event ){ $("#id_add_enquiry_slug").val( oo.fn.slug( $("#id_add_enquiry_title_en").val() ) ) });
	$("#add-enquiry").on("click", function(event){ event.preventDefault(); 
		oo.api.enquiry.add( {
			title_en:$("#id_add_enquiry_title_en").val(),
			title_fr:$("#id_add_enquiry_title_fr").val(),
			slug:$("#id_add_enquiry_slug").val(),
			enquete: $(this).attr("data-enquete-id")
		});
	});



};



oo.enquiry.upload = { enquiry_id:0 };

oo.enquiry.upload.init = function(){
	oo.log("[oo.enquiry.upload.init]");
	// blueimp upload for bulk attachments
	$('.fileupload').each( function(){

		$(this).fileupload({
			url: oo.api.urlfactory( 
				oo.api.urlfactory( oo.urls.upload_enquiry_pin, $(this).attr('data-enquiry-id') ),
				$(this).attr('data-pin-slug')
			),
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
			}
		});
	});
	// disabled by default
	// oo.glue.upload.disable();
}