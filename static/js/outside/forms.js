var oo = oo || {}; oo.forms = {};


oo.api.forms = {};

oo.api.forms.init = function( params ){
	$.mask.definitions['T'] = "[a-z0-9_.@-]"
	$.mask.definitions['S'] = "[a-zA-Z0-9_é,à,ê,â,ô,è,î,ï]"
	$.mask.definitions['E'] = "[a-zA-Z0-9_@.-]"
	$("input[name=username]").mask("TT?TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT", {placeholder:""});
	//$("input[name=email]").mask("EE?EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", {placeholder:""});
	$("input[name=affilation]").mask("SS?SSSSSSSSSSSSSSSSSSSSSS", {placeholder:""});
	
	
	
	$('input[name=password1], input[name=password2]').keyup(function(){
			
			if( $('input[name=password1]').val() != '' &&   $('input[name=password2]').val() != ''){
			
				if( $('input[name=password2]').val() != $('input[name=password1]').val() ) {
					
					$('#pass_confirm').html(oo.i18n.translate('the password is not the same as above')).removeClass().addClass('red');
				} else {
					$('#pass_confirm').html(oo.i18n.translate('Password confirmed')).removeClass().addClass('green');
					
				}
			}
		})
		
		$('input[name=password1]').keyup(function(){
			
			$('#security-pass').show()
		
			check = passwordStrength($('input[name=password1]').val(),$('input[name=username]').val())
		
			if( check == "Too short") {
				span_class = 'red'
			} else if( check == "Bad") {
				span_class = 'orange'
			} else if(check == "Good") {
				span_class = 'blue'
			} else if(check =="Strong") {
				span_class = 'green'
			
			} else if(check =="Too easy") {
				span_class = 'red'
			}
			
			html = $('<span/>')
				.addClass(span_class)
				.append(oo.i18n.translate(check))
			
			$('#result').html(html)
		})
		
		
		
		
		
		
	
}


function captcha_refresh(){

	$.ajax({
		url: oo.urls.captcha_refresh,
		dataType:'json',
		cache:false
	}).done(function(json) {
		$('img.captcha').attr('src', json.image_url)// This your should update captcha image src and captcha hidden input
   		$('input[name=captcha_0]').val(json.key)
   		
   		$('input[name=captcha_1]').val("")
   		
	});
	
    

   
	
}

$('.js-captcha-refresh').click(function(){
    captcha_refresh();
    return false;
});


