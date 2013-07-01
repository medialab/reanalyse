var oo = oo || {}; oo.subscriber = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.subscriber = {};
oo.magic.subscriber.add = function(){
	//oo.log("[oo.magic.subscriber.add]");
	$("#subscription").empty().hide();
	$("#subscription-accepted").show();
	$("#right-sidebar").height($("#subscription-accepted").height());
};

/*


    Subscriber Ajax API
    ===================

*/
oo.api.subscriber = {};
oo.api.subscriber.add = function( params ){
	/*if( params.accepted_terms == false){
		oo.toast( oo.i18n.translate("please check accepted terms"), oo.i18n.translate("form errors"));
		return;
	}*/
	
	
	var $this = $(this);
	if ($this.data("executing")) return;
	
	
    $this.data("executing", true)
    	//.attr("src", "/url/to/ajax-loader.gif");
	

	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_subscriber,
		data: params,
		
		success:function(result){
			
			if($("input[name=action]").val() == "EDIT"){
				oo.api.process( result, oo.magic.subscriber.add, "id_edit_profile" );
				
			} else {
				oo.api.process( result, oo.magic.subscriber.add, "id_subscriber" );
			}
			
			$this.removeData("executing");
			
		}
	}));
};




oo.subscriber.init = function(){
	oo.log("[oo.subscriber.init]");
	$("#add-subscriber, #edit-subscriber").click( function(){	oo.api.subscriber.add({
		first_name:$("input[name=first_name]").val(),
		last_name:$("input[name=last_name]").val(),
		affiliation:$("input[name=affiliation]").val(),
		description:$("textarea[name=description]").val(),
		accepted_terms:$("#id_subscriber_accepted_terms").prop("checked"),
		status:$('select[name=status]').val(),
		email:$("input[name=email]").val(),
		action:$("input[name=action]").val(),
		recaptcha_challenge_field:$('#recaptcha_challenge_field').val(),
		recaptcha_response_field:$('#recaptcha_response_field').val(),
	})});
	//$("").click()
};