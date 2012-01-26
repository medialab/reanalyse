window.onload = function(){
	
}

var xhrEngine = {
	sendNewRequest:function(url, callbackOnSuccess){
		var obj = {};
		var callback = function(){
			// 4 means the response has been returned and ready to be processed
			if (obj.readyState == 4) {
				// 200 means "OK"
				if (obj.status == 200) {
					// process whatever has been sent back here:
					callbackOnSuccess(obj.response);
					// anything else means a problem
				} else {
					alert("Error: there was a problem in the returned data (AJAX).\n");
				}
			}
		}
		if (window.XMLHttpRequest) {
			// obtain new object
			obj = new XMLHttpRequest();
			// set the callback function
			obj.onreadystatechange = callback;
			// we will do a GET with the url; "true" for asynch
			obj.open("GET", url, true);
			// null for GET with native object
			obj.send(null);
		// IE/Windows ActiveX object
		} else if (window.ActiveXObject) {
			obj = new ActiveXObject("Microsoft.XMLHTTP");
			if (obj) {
				obj.onreadystatechange = callback;
				obj.open("GET", url, true);
				// don't send null for ActiveX
				obj.send();
			}
		} else {
			alert("Your browser does not support AJAX");
		}
	},
	sendNewRequest_XML:function(url, callbackOnSuccess){
		var obj = {};
		var callback = function(){
			// 4 means the response has been returned and ready to be processed
			if (obj.readyState == 4) {
				// 200 means "OK"
				if (obj.status == 200) {
					// process whatever has been sent back here:
					callbackOnSuccess(obj.responseXML);
					// anything else means a problem
				} else {
					alert("Error: there was a problem in the returned data (AJAX).\n");
				}
			}
		}
		if (window.XMLHttpRequest) {
			// obtain new object
			obj = new XMLHttpRequest();
			// set the callback function
			obj.onreadystatechange = callback;
			// we will do a GET with the url; "true" for asynch
			obj.open("GET", url, true);
			// null for GET with native object
			obj.send(null);
		// IE/Windows ActiveX object
		} else if (window.ActiveXObject) {
			obj = new ActiveXObject("Microsoft.XMLHTTP");
			if (obj) {
				obj.onreadystatechange = callback;
				obj.open("GET", url, true);
				// don't send null for ActiveX
				obj.send();
			}
		} else {
			alert("Your browser does not support AJAX");
		}
	}
};

var parseGEXF = function(gexf){
	// Parse Attributes
	// This is confusing, so I'll comment heavily
	var nodesAttributes = [];	// The list of attributes of the nodes of the graph that we build in json
	var edgesAttributes = [];	// The list of attributes of the edges of the graph that we build in json
	var attributesNodes = gexf.getElementsByTagName("attributes");	// In the gexf (that is an xml), the list of xml nodes "attributes" (note the plural "s")
	for(i = 0; i<attributesNodes.length; i++){
		var attributesNode = attributesNodes[i];	// attributesNode is each xml node "attributes" (plural)
		if(attributesNode.getAttribute("class") == "node"){
			var attributeNodes = attributesNode.getElementsByTagName("attribute");	// The list of xml nodes "attribute" (no "s")
			for(ii = 0; ii<attributeNodes.length; ii++){
				var attributeNode = attributeNodes[ii];	// Each xml node "attribute"
				id = attributeNode.getAttribute("id");
				title = attributeNode.getAttribute("title");
				type = attributeNode.getAttribute("type");
				var attribute = {id:id, title:title, type:type};
				nodesAttributes.push(attribute);
				
			}
		} else if(attributesNode.getAttribute("class") == "edge"){
			var attributeNodes = attributesNode.getElementsByTagName("attribute");	// The list of xml nodes "attribute" (no "s")
			for(ii = 0; ii<attributeNodes.length; ii++){
				var attributeNode = attributeNodes[ii];	// Each xml node "attribute"
				var id = attributeNode.getAttribute("id");
				var title = attributeNode.getAttribute("title");
				var type = attributeNode.getAttribute("type");
				var attribute = {id:id, title:title, type:type};
				edgesAttributes.push(attribute);
				
			}
		}
	}
	
	var nodes = [];	// The nodes of the graph
	var nodesNodes = gexf.getElementsByTagName("nodes")	// The list of xml nodes "nodes" (plural)
	for(i=0; i<nodesNodes.length; i++){
		var nodesNode = nodesNodes[i];	// Each xml node "nodes" (plural)
		var nodeNodes = nodesNode.getElementsByTagName("node");	// The list of xml nodes "node" (no "s")
		for(ii=0; ii<nodeNodes.length; ii++){
			var nodeNode = nodeNodes[ii];	// Each xml node "node" (no "s")
			var id = nodeNode.getAttribute("id");
			var label = nodeNode.getAttribute("label") || id;
			var node = {id:id, label:label, attributes:[]};	// The graph node
			var attvalueNodes = nodeNode.getElementsByTagName("attvalue");
			for(iii=0; iii<attvalueNodes.length; iii++){
				var attvalueNode = attvalueNodes[iii];
				var attr = attvalueNode.getAttribute("for");
				var val = attvalueNode.getAttribute("value");
				node.attributes.push({attr:attr, val:val});
			}
			nodes.push(node);
		}
	}
	
	var edges = [];
	var edgesNodes = gexf.getElementsByTagName("edges");
	for(i=0; i<edgesNodes.length; i++){
		var edgesNode = edgesNodes[i];
		var edgeNodes = edgesNode.getElementsByTagName("edge");
		for(ii=0; ii<edgeNodes.length; ii++){
			var edgeNode = edgeNodes[ii];
			var source = edgeNode.getAttribute("source");
			var target = edgeNode.getAttribute("target");
			var edge = {id:ii, sourceID:source, targetID:target, attributes:[]};
			var attvalueNodes = edgeNode.getElementsByTagName("attvalue");
			for(iii=0; iii<attvalueNodes.length; iii++){
				var attvalueNode = attvalueNodes[iii];
				var attr = attvalueNode.getAttribute("for");
				var al = attvalueNode.getAttribute("value");
				edge.attributes.push({attr:attr, val:val});
			}
			edges.push(edge);
		}
	}
	
	graph = {nodesAttributes:nodesAttributes, edgesAttributes:edgesAttributes, nodes:nodes, edges:edges};
	$('#parsingResult').text("Your network has been parsed.");
	feedSiGMa();
}
