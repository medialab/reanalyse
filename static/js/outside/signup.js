var oo = oo || {}; oo.signup = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.signup = {};
oo.magic.signup.add = function(){
	oo.log("[oo.magic.subscriber.add]");
	$("#subscription").empty().hide();
	$("#subscription-accepted").show();
	$("#right-sidebar").height($("#subscription-accepted").height());
};

/*


    signup Ajax API
    ===================

*/



oo.api.signup = {};
oo.api.signup.add = function( params ){
	
	if( typeof oo.vars.enquete_id != "undefined"){
		$.extend( params, {enquete_id:oo.vars.enquete_id})
	}

	oo.log("[oo.api.signup.add]", params);

	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_signup,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.signup.add] result:", result );
			
			if(result.status != 'ok' && result.code=="IntegrityError"){
				return oo.toast( oo.i18n.translate("error"), oo.i18n.translate("error") );
			}

			oo.api.process( result, oo.magic.signup.add, "id_signup" );
		}
	}));
};


oo.signup.init = function(){oo.log("[oo.signup.init]");
	
	$("#add-signup").click( function(){
		
		
		oo.api.signup.add({

			username:$('input[name=username]').val(),
			first_name:$('input[name=first_name]').val(),
			last_name:$('input[name=last_name]').val(),
			email:$('input[name=email]').val(),
			affiliation:$('input[name=affiliation]').val(),
			password:$('input[name=password]').val(),
			status:$('select[name=status]').val(),
			message:$('#id_signup_message').val(),
			accepted_terms:$('input[name=accepted_terms]').val(),
			recaptcha_challenge_field:$('input[name=recaptcha_challenge_field]').val(),
			recaptcha_response_field:$('input[name=recaptcha_response_field]').val(),
	})});
	//$("").click()
};
