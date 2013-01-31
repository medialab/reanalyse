var oo = oo || {}; oo.subscriber = {};

/*


    Magic
    =====

*/
oo.magic = oo.magic || {};
oo.magic.subscriber = {};
oo.magic.subscriber.add = function(){
	oo.log("[oo.magic.subscriber.add]");
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
	if( params.accepted_terms == false){
		oo.toast( oo.i18n.translate("please check accepted terms"), oo.i18n.translate("form errors"));
		return;
	}

	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.add_subscriber,
		data: params, 
		success:function(result){
			oo.log( "[oo.api.subscriber.add] result:", result );
			oo.api.process( result, oo.magic.subscriber.add, "id_subscriber" );
		}
	}));
};


oo.subscriber.init = function(){
	oo.log("[oo.subscriber.init]");
	$("#add-subscriber").click( function(){oo.api.subscriber.add({
		first_name:$("#id_subscriber_first_name").val(),
		last_name:$("#id_subscriber_last_name").val(),
		affiliation:$("#id_subscriber_affiliation").val(),
		description:$("#id_subscriber_description").val(),
		accepted_terms:$("#id_subscriber_accepted_terms").prop("checked"),
		status:$("#id_subscriber_status").val(),
		email:$("#id_subscriber_email").val(),
		recaptcha_challenge_field:$('#recaptcha_challenge_field').val(),
		recaptcha_response_field:$('#recaptcha_response_field').val(),
	})});
	//$("").click()
};