// testing / debugging
var d=null;
var dat=null;
var test=null;

////////////////////////////////////////////////////
function buildD3_ParaverbalTimeline(thedata,theId) {
	dat = thedata;
	
	var maxWords = thedata.totalwords;
	var maxParaverbal = thedata.paraverbaltypes.length;
	console.log("maxWords:"+maxWords);
	console.log("theId:"+theId);
	
	var wStep = 40; // space for words
	var pStep = 15; // space for each paraverbal
	var ldec = 5;	// decalage for labels
	
	// paraverbal png images
	var pngUrl = "/reanalyse/media/images/";
	var pngW = 18;
	var pngH = 15; 
	
	var totalW = 600;
	
	//var totalH=250;
	
	var leftMargin=100; // for yLabels
	
	var rW = totalW + leftMargin;
	var rH = wStep + pStep*maxParaverbal;
	
	console.log("Size:"+rW+":"+rH);
	
	/////////// GENERAL CHART
	var vis = d3.select("#"+theId).append("svg:svg")
		.attr("width",rW)
		.attr("height",rH+20);
		//.attr("viewBox","0 0 "+rW+" "+rH);
	var chart = vis.append("svg:g")
		.attr("background-color","steelblue");
	chart.append("svg:rect")
		.attr("stroke","gray")
		.attr("fill","lightgray")
		.attr("x",leftMargin)
		.attr("y",0)
		.attr("width",totalW)
		.attr("height",rH);
	var timeline = chart.append("svg:g");
	
	////////////////////////////////////////////////////////////////////
	/////////// X scale
	var xWordScale = d3.scale.linear()
		.domain([0,maxWords])
		.range([0,totalW]);
	var yParaverbalScale = function(k) {
		return wStep + pStep*k;
	};

	/////////// LEGEND LABELS on left
	timeline.append("svg:text")
		.attr("class","label")
		.attr("x",leftMargin-2*ldec)
		.attr("y",wStep/2)
		.attr("text-anchor", "end")
		.text("Words");
	var parLines = timeline.selectAll("pLines")
		.data(thedata.paraverbaltypes)
		.enter().append("svg:line")
			.attr("x1",leftMargin)
			.attr("x2",rW)
			.attr("y1",function (d,i){return yParaverbalScale(i);})
			.attr("y2",function (d,i){return yParaverbalScale(i);})
			.attr("stroke", "black");
	var parLabels = timeline.selectAll("pLabels")
		.data(thedata.paraverbaltypes)
		.enter().append("svg:text")
			.attr("class", "label")
			.attr("x", leftMargin-2*ldec-pngW)
			.attr("y", function (d,i){return yParaverbalScale(i)+3+pStep/2;} )
			.attr("text-anchor", "end")
			.text( function(d,i){return d;} );
	var parImgs = timeline.selectAll("pImgs")
		.data(thedata.paraverbaltypes)
		.enter().append("svg:image")
			.attr("x", leftMargin-ldec-pngW)
			.attr("y", function (d,i){return yParaverbalScale(i);} )
			.attr("width",pngW)
			.attr("height",pngH)
			.attr("xlink:href", function (d) { return pngUrl+"text_"+d+".png";} );
			
	/////////// LINES for paraverbal
	var parLines = timeline.selectAll("pLines")
		.data(thedata.paraverbal)
		.enter().append("svg:line")
			.attr("y1", function (d,i){return yParaverbalScale(d.paraverbal);} )
			.attr("y2", function (d,i){return yParaverbalScale(d.paraverbal)+pStep;} )
			.attr("x1", function (d,i){return leftMargin + xWordScale(d.count);} )
			.attr("x2", function (d,i){return leftMargin + xWordScale(d.count);} )
			.attr("stroke", "black");

	/////////// IF TIME, then also showing text
	// build an array with only time data 
	timeIndex = thedata.paraverbaltypes.indexOf('time');
	var timeData = new Array();
	thedata.paraverbal.forEach( function(d) {
		if(d.paraverbal==timeIndex) timeData.push(d);
	});
	var parTimeText = timeline.selectAll("pTime")
		.data(timeData)
		.enter().append("svg:text")
			.attr("y", function (d,i){return yParaverbalScale(d.paraverbal)+30;} )
			.attr("x", function (d,i){return leftMargin + xWordScale(d.count);} )
			.attr("text-anchor", "middle")
			.text( function (d,i){return d.content;} );

	/////////// STACKED RECTS for words, manually
	var words = timeline.selectAll("words")
		.data(thedata.speakers)
		.enter().append("svg:rect")
		.attr("y", 0)
		.attr("x", function(d) {return leftMargin + xWordScale(d.in);} )
		.attr("height", wStep)
		.attr("width", function(d) {return xWordScale(d.out-d.in);} )
		.attr("class", function(d) {return "speakerColor_"+d.id;});
		
};
////////////////////////////////////////////////////