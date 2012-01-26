// testing / debugging
var d=null;
var dat=null;
var test=null;

////////////////////////////////////////////////////
function buildD3_SpeakersByText(thedata,theId) {
	//console.log("D3:buidling from data");
	
	dat = thedata;
	///////////
	// Size of rect ! not of svg graphic
	
	var nSpeakers = thedata.speakers.length;
	var nTexts = thedata.texts.length;

	var totalW=450;
	var totalH=30+nSpeakers*7;
		
	var wStep=totalW/nTexts; // step between bars
	var maxWords = thedata.maxWords*6/5; // to make graph a little taller than real data

	var leftMargin=45; // for yLabels
	var rightMargin=100;
	var bottomMargin=50; // for xLabels
	var topInMargin=50; // in graph
	var rectsWidth=wStep-7; // for bars

	//console.log("nTexts: "+nTexts);
	//console.log("nSpeakers: "+nSpeakers);
	//console.log("maxWords: "+maxWords);
	
	var rW = totalW + leftMargin + rightMargin;
	var rH = totalH + bottomMargin;
	/////////// GENERAL CHART
	var vis2 = d3.select("#"+theId).append("svg:svg")
		//.attr("width", totalW + leftMargin + rightMargin)
		//.attr("height", totalH + bottomMargin);
		.attr("viewBox","0 0 "+rW+" "+rH);
	var chart = vis2.append("svg:g")
		.attr("background-color","steelblue")
		.attr("transform", "translate(0,20)");
	chart.append("svg:rect")
		.attr("stroke","gray")
		.attr("fill","lightgray")
		.attr("x",leftMargin)
		.attr("y",0)
		.attr("width",totalW)
		.attr("height",totalH);
	var view_texts = chart.append("svg:g")
	///////////////////////////////////////////////////////////////////////////////////////////////////
	/////////// X Y scales
	var x = d3.scale.linear()
		.domain([0,100])
		.range([0, totalW]);
	var y_words = d3.scale.linear()
		.domain([0,maxWords])
		.range([0,totalH]);
	var x_steps = function (d,i) { return leftMargin + wStep/2 + i * wStep; };
	
	/////////// Y LABELS (Words)
	var ylabels = view_texts.selectAll("yLabel")
		.data(y_words.ticks(5))
		.enter().append("svg:text")
			.attr("class", "label")
			.attr("x", leftMargin/2 )
			.attr("y", function (d,i){return totalH - y_words(d,i);} )
			.attr("text-anchor", "middle")
			.text( function(d,i){return d;} );
	/////////// Y Lines (Words)
	var ylines = view_texts.selectAll("yLines")
		.data(y_words.ticks(10))
		.enter().append("svg:line")
			.attr("y1", function (d,i){return totalH - y_words(d,i);} )
			.attr("y2", function (d,i){return totalH - y_words(d,i);} )
			.attr("x1", leftMargin - 4)
			.attr("x2", totalW + leftMargin)
			.attr("stroke", "gray");
			
	/////////// RECT for WORDCOUNT & WORDENTITY COUNT
/*
	view_texts.selectAll("TextsAllWords")
		.data(thedata.texts)
		.enter().append("svg:rect")
			.attr("fill","steelblue")
			.attr("x", function (d,i){return leftMargin + wStep/2 + i * wStep - rectsWidth/2;} )
			.attr("y", totalH )
			.attr("width", rectsWidth )
			.attr("height", 0 )
			.transition()
				.duration(400)
				.attr("y", function(d,i){return totalH - y_words(d.count);} )
				.attr("height", function(d,i){ return y_words(d.count);} );
*/
	
	/////////// STACKED LAYOUT
	/*
	
	thedata.data is an array [ S1, S2, S3 ] :
	where S1 = [ {x:0,y:nWordsForText0}, {x:1,y:nWordsForText1}, ... ]
	where S2 = ...
	
	*/
	
	var stData = d3.layout.stack()(thedata.data);
	
	//var speakerColor = d3.interpolateRgb("#339966", "#FFFF66");
	//var speakerColor = d3.scale.category20();
	// color is rather made from speaker.id !!
	
	var x = function(d,i) { return leftMargin - rectsWidth/2 + wStep/2 + i*wStep; };
	var maxStackedWords = d3.max(stData, function(d) {     return d3.max(d, function(d) {return d.y0 + d.y;});    } ) * 6/5;
	var y0 = function(d) { return totalH - d.y0 * totalH / maxStackedWords; };
	var y1 = function(d) { return totalH - (d.y + d.y0) * totalH / maxStackedWords; };
	
	var layers = view_texts.selectAll("g.layer")
		.data(stData)
		.enter().append("svg:g");
	var bars = layers.selectAll("g.bar")
		.data(function(d) { return d; })
		.enter().append("svg:g")
		.attr("transform", function(d,i) { return "translate(" + x(d,i) + ",0)"; });
	bars.append("svg:rect")
		.attr("width", rectsWidth)
		.attr("x", 0)
		.attr("y", y1)
		.attr("height", function(d) { return y0(d) - y1(d); })
		.attr("stroke", "gray")
		.attr("class", function(d) {return "speakerColor_"+d.id;});
	
	/////////// SPEAKERS COLOR LEGEND
	var colRectW = 10;
	var rightRectMargin = 10;
	var ySpeakers = d3.scale.linear()
		.range([totalH, 0]);
	chart.selectAll("SpeakerNames")
		.data(thedata.speakers)
		.enter().append("svg:text")
			.attr("x", leftMargin + totalW + rightRectMargin + colRectW + 5 )
			.attr("y",function(d,i){return ySpeakers(i/nSpeakers) + colRectW;} )
			.text(function(d,i){return d.name;});
	chart.selectAll("SpeakerColors")
		.data(thedata.speakers)
		.enter().append("svg:rect")
			.attr("class", function(d) {return "speakerColor_"+d.id;})
			.attr("x", leftMargin + totalW + rightRectMargin )
			.attr("y",function(d,i){return ySpeakers(i/nSpeakers);} )
			.attr("width", colRectW)
			.attr("height", colRectW);
						
	/////////// TEXT X LABELS : DISPLAY TEXT NAMES (xLabels)
	// TODO: rather try to make a textArea object to break lines in case of too long names
	chart.selectAll("TextNames")
		.data(thedata.texts)
		.enter().append("svg:text")
			//.attr("width",100)
			//.attr("height",100)
			//.attr("font-size",25)
			//.attr("font-family","Georgia")
			.attr("x", x_steps )
			.attr("y", totalH + 20 )
			.attr("text-anchor","middle")
			.text( function(d,i) {return d.id;} );
};
////////////////////////////////////////////////////