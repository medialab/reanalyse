var oo = oo || {}; oo.reinitialize_password = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.reinitialize_password = {};
oo.magic.reinitialize_password.launch = function(){
	oo.log("[oo.magic.reinitialize.launch]");
	
};

/*


    signup Ajax API
    ===================

*/

oo.api.reinitialize_password = {};

oo.api.reinitialize_password.launch = function( params ){
	
	var $this = $(this);
	if ($this.data("executing")) return;
	
	
    $this.data("executing", true)
    	//.attr("src", "/url/to/ajax-loader.gif");
    
	
	
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.reinitialize_password,
		data: params,
		success:function(result){
			
			if(result.status != 'ok' && result.code=="IntegrityError"){
				$this.removeData("executing");
				return oo.toast( oo.i18n.translate("error"), oo.i18n.translate("error") );
			}
			
			if(result.status == 'ok'){
				$("#subscription").empty().hide();
				$("#subscription-accepted").show();
				$("#right-sidebar").height($("#left-side").height());
				
			} else if( result.error == 'password not valid' ) {
				oo.api.process( result, oo.magic.change_password.add, "id_reinitialize_password" );
				
			}
			
			oo.api.process( result, oo.magic.change_password.add, "id_reinitialize_password" );	

			$this.removeData("executing");
		}
	}));
};

oo.api.reinitialize_password.init = function(){
	$("#reinitialize-password").click( function(){
		
		oo.api.reinitialize_password.launch({
			username:$('input[name=username]').val(),
			email:$('input[name=email]').val(),
			captcha_0:$('input[name=captcha_0]').val(),
			captcha_1:$('input[name=captcha_1]').val(),
			
		
		})});
	//$("").click()
};
