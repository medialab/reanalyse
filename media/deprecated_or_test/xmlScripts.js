

////////////////////////////////////////////////
function loadXMLDoc(dname) {
	if (window.XMLHttpRequest)
	  {
	  xhttp=new XMLHttpRequest();
	  }
	else
	  {
	  xhttp=new ActiveXObject("Microsoft.XMLHTTP");
	  }
	xhttp.open("GET",dname,false);
	xhttp.send("");
	return xhttp.responseXML;
}
////////////////////////////////////////////////
// 2 javascript functions to load XML files with an XSL Transformation
function displayXMLFile() {
	xml=loadXMLDoc("/pools/media/xml/ReanE_example.xml");
	xsl=loadXMLDoc("/pools/media/xml/ReanE.xsl");
	// code for IE
	if (window.ActiveXObject)
	  {
	  ex=xml.transformNode(xsl);
	  document.getElementById("xmlDiv").innerHTML=ex;
	  }
	// code for Mozilla, Firefox, Opera, etc.
	else if (document.implementation && document.implementation.createDocument)
	  {
	  xsltProcessor=new XSLTProcessor();
	  xsltProcessor.importStylesheet(xsl);
	  resultDocument = xsltProcessor.transformToFragment(xml,document);
	  document.getElementById("xmlDiv").appendChild(resultDocument);
	  }
}
////////////////////////////////////////////////





//////////////////////////////////////////////////
// manage collapsable divs for texts
jQuery(document).ready(function(){
	//displayXMLFile();
	$(function() {
		$( "#xmlTextAccordion" ).accordion();
	});
	
//	$('#xmlTextAccordion .h3').click(function() {
//		$(this).next().toggle('slow');
//		return false;
//	}).next().hide();
});
//////////////////////////////////////////////////