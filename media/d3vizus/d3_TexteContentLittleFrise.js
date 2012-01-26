////////////////////////////////////////////////////
/*
	thedata['maxCurrent']
	thedata['maxGlobal']
	thedata['speakers'] = [ {'id':speakerid,'from':nCumulated,'count':nSentences,'name':spName} for each speaker ]
*/
////////////////////////////////////////////////////
function buildD3_TexteContentLittleFrise(thedata,theId) {
	var totalW=80;
	
	var maxCurrent = thedata.maxCurrent;
	var maxGlobal = thedata.maxGlobal;
	
	var svgvis = d3.select("#"+theId).append("div")
		.attr("class","vizdiv");
	svgvis = svgvis.append("svg:svg")
		.attr("width", totalW)
		.attr("height", 10);
		
	var rects = svgvis.append("svg:g")

	rects.selectAll("theRects")
		.data(thedata.speakers)
		.enter().append("svg:rect")
			.attr("title", function(d) {return d.name;})
			.attr("class", function(d) {return "speakerColor_"+d.id;})
			.attr("x", function (d,i){return d.from*totalW/maxGlobal;} )
			.attr("y", 0 )
			.attr("width", function (d,i){return d.count*totalW/maxGlobal;} )
			.attr("height", 10 );
/*
			.transition()
				.duration(400)
				.attr("y", function(d,i){return totalH - y_words(d.count);} )
				.attr("height", function(d,i){ return y_words(d.count);} );
*/

	rects.append("svg:rect")
		.attr("stroke", "gray")
		.attr("fill","transparent")
		.attr("x", 0 )
		.attr("y", 0 )
		.attr("width", function (d,i){return maxCurrent*totalW/maxGlobal;} )
		.attr("height", 10 );
};
////////////////////////////////////////////////////






////////////////////////////////////////////////////
// UNUSED FOR THE MOMENT ?
////////////////////////////////////////////////////
/*
	thedata['maxCurrent']
	thedata['maxGlobal']
	thedata['speakers'] = [ {'id':speakerid,'from':nCumulated,'count':nSentences,'name':spName} for each speaker ]
*/
////////////////////////////////////////////////////
function buildD3_TexteContentLittleRect(thedata,theId) {
	var totalW=80;
	var maxGlobal = thedata.maxGlobal;
	
	var svgvis = d3.select("#"+theId).append("svg:svg")
		.attr("width", totalW)
		.attr("height", 10);
	var rects = svgvis.append("svg:g")

	rects.append("svg:rect")
		.attr("title", function(d) {return d.name;})
		.attr("class", function(d) {return "speakerColor_"+d.id;})
		.attr("x", 0 )
		.attr("y", 0 )
		.attr("width", 0 )
		.attr("height", 10 )
		.transition()
			.duration(400)
			.attr("width", thedata.maxCurrent * totalW / thedata.maxGlobal );
};
////////////////////////////////////////////////////