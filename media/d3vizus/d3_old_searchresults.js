////////////////////////////////////////////////////
function buildD3GraphFromData(theData) {
	//console.log("D3:buidling from data");
	
	theTextes = theData[0];
	theSpeakers = theData[1];
	thedata = theData[2];
	
	///////////
	var maxTextes = theTextes.length ;
	var maxSpeakers = theSpeakers.length ;
	var leftMargin=130;
	var topMargin=5;	
	var totalW=700;
	var totalH=30+Math.max(maxSpeakers,maxTextes)*10 + 2*topMargin;
	var tStep=totalH/maxTextes;
	var sStep=totalH/maxSpeakers;
	var bezierDec=220;
	var bezierMargin=5;
	
	/////////// GENERAL CHART
	var chart = d3.select("#d3stats").append("svg:svg")
		.attr("width", totalW)
		.attr("height", totalH)
	/////////////////////////////////////////////////
	var dcons = totalH - topMargin ; 
	var dfact = totalH - 2*topMargin;
	var yTextes = function(d,i) {
		return dcons - tStep/2 - i*dfact/maxTextes;
	}
	var ySpeakers = function(d,i) {
		return dcons - sStep/2 - i*dfact/maxSpeakers;
	}
	/////////// LABELS
	var tLabels = chart.selectAll("tLabel")
		.data(theTextes)
		.enter().append("svg:text")
			.attr("class", "label")
			.attr("x", leftMargin )
			.attr("y", function(d,i){return 2+yTextes(d,i);} )
			.attr("text-anchor", "end")
			.text( function(d,i){return d;} );
	var sLabels = chart.selectAll("sLabel")
		.data(theSpeakers)
		.enter().append("svg:text")
			.attr("class", "label")
			.attr("x", totalW-leftMargin )
			.attr("y", function(d,i){return 2+ySpeakers(d,i);} )
			.attr("text-anchor", "left")
			.text( function(d,i){return d;} );
	sLabels.append("svg:circle")
		.attr("r", 4.5);
				
	///////////
	var link = chart.selectAll("path.link")
		.data(thedata)
		.enter().append("svg:path")
		.attr("class", "svgLinkTextSpeaker")
		.attr("d", function(d,i) {
			var xT = leftMargin+bezierMargin;
			var xS = totalW-leftMargin-bezierMargin ;
			var yT = yTextes(0,d[0]);
			var yS = ySpeakers(0,d[1]);
			return "M "+xT+" "+yT+" C "+(xT+bezierDec)+" "+yT+" "+(xS-bezierDec)+" "+yS+" "+xS+" "+yS;
		});		
};
////////////////////////////////////////////////////