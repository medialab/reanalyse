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
			enquete: $("#id_add_enquiry_enquete").val()
		});
	});

};