function buildXmlDisplay(divid,xmlurl) {
	console.log("Building XML tree: "+xmlurl);
	
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
			
			// todo: close every node on load..
			// pb is that jstree doesn't provide onLoaded() callback !
			//$("#divid").jstree("close_all");
			//$("#xml_tei_bfm_div").jstree("close_all");
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
