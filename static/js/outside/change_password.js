var oo = oo || {}; oo.change_password = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.change_password = {};
oo.magic.change_password.add = function(){
	oo.log("[oo.magic.change_password.add]");
	
};

/*


    signup Ajax API
    ===================

*/

oo.api.change_password = {};

oo.api.change_password.add = function( params ){

	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.change_password,
		data: params, 
		success:function(result){
			
			if(result.status != 'ok' && result.code=="IntegrityError"){
				return oo.toast( oo.i18n.translate("error"), oo.i18n.translate("error") );
			}
			
			if(result.status == 'ok'){
				$("#subscription").empty().hide();
				$("#subscription-accepted").show();
				$("#right-sidebar").height($("#left-side").height());
				
			} else if( result.error == 'password not valid' ) {
				oo.api.process( result, oo.magic.change_password.add, "id_change_password" );
				
			}
			
			oo.api.process( result, oo.magic.change_password.add, "id_change_password" );	

			
		}
	}));
};

oo.change_password.init = function(){
	$("#change-password").click( function(){
		
		if( $('input[name=password1]').val() != $('input[name=password2]').val() ){
			return oo.toast( oo.i18n.translate("the two fields are not the same string"), oo.i18n.translate("error") );
		}
		
		oo.api.change_password.add({
			username:$('input[name=username]').val(),
			password1:$('input[name=password1]').val(),
			password2:$('input[name=password2]').val(),
			recaptcha_challenge_field:$('input[name=recaptcha_challenge_field]').val(),
			recaptcha_response_field:$('input[name=recaptcha_response_field]').val(),
			
		
	})});
	//$("").click()
};
