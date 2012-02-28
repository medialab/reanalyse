function buildXmlDisplay(divid,xmlurl) {
	//console.log("Building XML tree: "+xmlurl);
	
	$.ajax({
		type: "GET",
		url: xmlurl,
		dataType:"xml",
		cache: false,
		beforeSend:function(){
			//do something before send
		},
		success: function(data){
			var _uimTree = new UIMTreeProcessor(data, $("#"+divid));
			_uimTree.doProcess();
			//processXML(data);
			
			// to set nodes closed on load, set 'state':closed in UIMTreeProcessor.js
			
			// the following is not working
			//$("#"+divid).jstree("close_all");
			
			// global func to update left menu size
			dime.updateView();
		},
		error:function(e){
			alert("Error: "+e);
		}
	});	
		
	
/*
	$("#"+divid).jstree({
		"xml_data":{
			"ajax":{"url":xmlurl},
			"xsl":"nest"
			},
		"plugins":["themes", "xml_data"]
	});
*/
};
