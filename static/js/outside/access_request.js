var oo = oo || {}; oo.access_request = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.access_request = {};
oo.magic.access_request.add = function(){
	oo.log("[oo.magic.access-request.add]");
	
};

/*
    AccessRequest Ajax API
    ===================
*/



oo.api.access_request = {};
oo.api.access_request.add = function( params ){
	
	if( typeof oo.vars.enquete_id != "undefined"){
		$.extend( params, {enquete_id:oo.vars.enquete_id})
	}

	oo.log("[oo.api.signup.add]", params);
	
	var $this = $(this);
	if ($this.data("executing")) return;
	
	
    $this.data("executing", true)
    	//.attr("src", "/url/to/ajax-loader.gif");
    
	
	
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.outside_access_request,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.signup.add] result:", result );
			
			if(result.status != 'ok' && result.code=="IntegrityError"){
				return oo.toast( oo.i18n.translate("error"), oo.i18n.translate("error") );
			}
			
			if(result.status == 'ok'){
				$("#subscription").empty().hide();
				$("#subscription-accepted").show();
				$("#right-sidebar").height($("#left-side").height());
				
			}

			oo.api.process( result, oo.magic.access_request.add, "id_access_request" );
			
			$this.removeData("executing");
		}
	}));
};


oo.access_request.init = function(){oo.log("[oo.access_request.init]");
	
	$("#add-access-request").click( function(){
		oo.api.access_request.add({
			username:	$('input[name=username]').val(),
			first_name:	$('input[name=first_name]').val(),
			last_name:	$('input[name=last_name]').val(),
			email:		$('input[name=email]').val(),
			affiliation:$('input[name=affiliation]').val(),
			password:	$('input[name=password]').val(),
			status:		$('select[name=status]').val(),
			description:$('#id_access_request_description').val(),
			enquete:!$('#id_access_request_enquete').is("select")?$('input[name=enquete]').val():$('select[name=enquete]').val(),
			accepted_terms:	$('input[name=accepted_terms]').val(),
			captcha_0:$('input[name=captcha_0]').val(),
			captcha_1:$('input[name=captcha_1]').val(),
	})});
	//$("").click()
};
