var oo = oo || {}; oo.signup = {};

/*


    Magic
    =====

*/

oo.requestRunning = false;
oo.magic = oo.magic || {};
oo.magic.signup = {};
oo.magic.signup.add = function(){
	//oo.log("[oo.magic.subscriber.add]");
	$("#subscription").empty().hide();
	$("#subscription-accepted").show();
	$("#right-sidebar").height($("#left-side").height());
};

/*
    signup Ajax API
    ===================
*/


oo.api.signup = {};
oo.api.signup.add = function( params ){
	
	if( params.accepted_terms == false){
		oo.toast( oo.i18n.translate("please check accepted terms"), oo.i18n.translate("form errors"));
		return;
	}
	
	password1 = $('input[name=password1]').val()
	password2 = $('input[name=password2]').val()
	
	
	if(  password1 != password2){
		return oo.toast( oo.i18n.translate("the two fields are not the same string"), oo.i18n.translate("error") );
	} else {
		
		if(  passwordStrength($('#id_signup_password1').val(),$('#id_signup_username').val()) == 'Too short'
			|| passwordStrength($('#id_signup_password1').val(),$('#id_signup_username').val()) == 'Bad'
			|| passwordStrength($('#id_signup_password1').val(),$('#id_signup_username').val()) == 'Too easy' 
		
		) {
			return oo.toast( oo.i18n.translate("Your password security is too weak"), oo.i18n.translate("error") );
			
		}
		
	}
	
	
	
	if( typeof oo.vars.enquete_id != "undefined"){
		$.extend( params, {enquete_id:oo.vars.enquete_id})
	}

	//oo.log("[oo.api.signup.add]", params);
	
	var $this = $(this);
	if ($this.data("executing")) return;
	
    $this.data("executing", true)
    	//.attr("src", "/url/to/ajax-loader.gif");	
	
	$('#signup').append('<span class="ajax-loader"></span>')
	

	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_signup,
		data: params,
		
		success:function(result){
			oo.log( "[oo.api.signup.add] result:", result );

			oo.api.process( result, oo.magic.signup.add, "id_signup" );
			
			$('.ajax-loader').remove()
			
			$this.removeData("executing");
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
			password1:$('input[name=password1]').val(),
			password2:$('input[name=password2]').val(),
			status:$('select[name=status]').val(),
			description:$('textarea[name=description]').val(),
			accepted_terms:$('input[name=accepted_terms]').prop("checked"),
			recaptcha_challenge_field:$('input[name=recaptcha_challenge_field]').val(),
			captcha_0:$('input[name=captcha_0]').val(),
			captcha_1:$('input[name=captcha_1]').val(),
			
	})});
};
