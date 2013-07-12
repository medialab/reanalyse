var oo = oo || {}; oo.login = {};

/*


    Magic
    =====

*/

oo.requestRunning = false;
oo.magic = oo.magic || {};
oo.magic.login = {};
oo.magic.login.add = function(){
	//oo.log("[oo.magic.subscriber.add]");
	/*$("#subscription").empty().hide();
	$("#subscription-accepted").show();
	$("#right-sidebar").height($("#left-side").height());*/
	
};

/*
    login Ajax API
    ===================
*/


oo.api.login = {};
oo.api.login.add = function( params ){

	var $this = $(this);
	if ($this.data("executing")) return;
	
    $this.data("executing", true)
	
	
	
	$('#login-button').parent().append('<span class="ajax-loader"></span>')
	

	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.login,
		data: params,
		
		success:function(result){
			oo.log( "[oo.api.login.add] result:", result );

			oo.api.process( result, oo.magic.login.add, "id_login" );
			
			$('.ajax-loader').remove()
			
			$(location).attr('href',result.next);
			
			$this.removeData("executing");
		}
	}));
};


oo.login.init = function(){oo.log("[oo.login.init]");
	oo.log('login')
	
	$("#login-button").click( function(){

		oo.api.login.add({
			username:$('input[name=username]').val(),
			password:$('input[name=password]').val(),
			captcha_0:$('input[name=captcha_0]').val(),
			captcha_1:$('input[name=captcha_1]').val(),
			next:$('input[name=next]').val(),
			
	})
	
	return false;
	}
	
	
	
	);
	
	
};
