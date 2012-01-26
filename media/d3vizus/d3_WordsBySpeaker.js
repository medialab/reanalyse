// testing / debugging
var d=null;
var test=null;

var view_words;
var view_tfidf;
var hiddenOpacity=0.15;
////////////////////////////////////////////////////
function initD3TextDefaultValues() { // trigerred when all objects are created
	switchTextView('view_words');
}
////////////////////////////////////////////////////
function switchTextView(viewName) {
	//console.log("switching mode:"+viewName);
	if(viewName=='view_words') {
		view_words.attr("opacity","1");
		$('#id_view_words').attr("class","d3buttonOn");
		view_tfidf.attr("opacity",hiddenOpacity);
		$('#id_view_tfidf').attr("class","d3buttonOff");
	}
	if(viewName=='view_tfidf') {
		view_tfidf.attr("opacity","1");
		$('#id_view_tfidf').attr("class","d3buttonOn");
		view_words.attr("opacity",hiddenOpacity);
		$('#id_view_words').attr("class","d3buttonOff");
	}
	//viewobj.attr("visibility","hidden");
	//viewobj.attr("visibility","visible");
}
////////////////////////////////////////////////////
function buildD3_WordsBySpeaker(thedata,theId) {
	//console.log("D3:buidling from data");
	
	// make buttons
	var ulButts = d3.selectAll("#"+theId)
		.insert("div","#d3stats")
		.insert("ul")
			.attr("class","d3buttons");
	ulButts.append("li")
		.on("click",function(){switchTextView('view_words');})
		.attr("class","d3buttonOn")
		.attr("id","id_view_words")
		.text("Show Word Counts");
	ulButts.append("li")
		.on("click",function(){switchTextView('view_tfidf');})
		.attr("class","d3buttonOff")
		.attr("id","id_view_tfidf")
		.text("Show TFIDFs");			

	d = thedata;
	///////////
	// Size of rect ! not of svg graphic
	var totalW=550;
	var totalH=170;
	var wStep=totalW/thedata.speakers.length; // step between bars
	var maxWords = d3.max( thedata.speakers, function(d,i) { return Math.max( parseInt(d.wordentitycount),parseInt(d.wordcount) ); });
	var maxWords = maxWords*6/5 ; // to make graph a little taller than real data
	var maxTfidf = d3.max( thedata.words, function(d,i) { return d.tfidf; } );
	var maxTfidf = maxTfidf*6/5 ; // same same
	var leftMargin=70; // for yLabels
	var bottomMargin=50; // for xLabels
	var topInMargin=50; // in graph
	var rectsWidth=30; // for bars
	//var maxTfidf = todo;
	//console.log("wStep: "+wStep);
	//console.log("maxWords: "+maxWords);
	//console.log("maxTfidf: "+maxTfidf);
	
	var rW = totalW + leftMargin;
	var rH = totalH + bottomMargin;
	/////////// GENERAL CHART
	var vis2 = d3.select("#"+theId).append("svg:svg")
		//.attr("width", totalW + leftMargin)
		//.attr("height", totalH + bottomMargin)
		.attr("viewBox","0 0 "+rW+" "+rH);
		//.attr("viewBox","0 0 20 50");
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
	view_words = chart.append("svg:g")
	view_tfidf = chart.append("svg:g")
	///////////////////////////////////////////////////////////////////////////////////////////////////
	/////////// X Y scales
	var x = d3.scale.linear()
		.domain([0,100])
		.range([0, totalW]);
	var y_tfidf = d3.scale.linear()
		.domain([0,100])
		.range([0, totalH]);
	var y_words = d3.scale.linear()
		.domain([0,maxWords])
		.range([0,totalH]);
	var x_steps = function (d,i) { return leftMargin + wStep/2 + i * wStep; };
	
	/////////// Y LABELS (Words)
	var ylabels = view_words.selectAll("yLabel")
		.data(y_words.ticks(5))
		.enter().append("svg:text")
			.attr("class", "label")
			.attr("x", leftMargin/2 )
			.attr("y", function (d,i){return totalH - y_words(d,i);} )
			.attr("text-anchor", "middle")
			.text( function(d,i){return d;} );
	/////////// Y Lines (Words)
	var ylines = view_words.selectAll("yLines")
		.data(y_words.ticks(10))
		.enter().append("svg:line")
			.attr("y1", function (d,i){return totalH - y_words(d,i);} )
			.attr("y2", function (d,i){return totalH - y_words(d,i);} )
			.attr("x1", leftMargin - 4)
			.attr("x2", totalW + leftMargin)
			.attr("stroke", "gray");
			
	/////////// RECT for WORDCOUNT & WORDENTITY COUNT
	view_words.selectAll("SpeakerRectsWords")
		.data(thedata.speakers)
		.enter().append("svg:rect")
			.attr("fill","steelblue")
			.attr("x", function (d,i){return leftMargin + wStep/2 + i * wStep - rectsWidth/2;} )
			.attr("y", totalH )
			.attr("width", rectsWidth )
			.attr("height", 0 )
			.transition()
				.duration(400)
				.attr("y", function(d,i){return totalH - y_words(d.wordcount);} )
				.attr("height", function(d,i){ return y_words(d.wordcount);} );
	view_words.selectAll("SpeakerRectsWordEntities")
		.data(thedata.speakers)
		.enter().append("svg:rect")
			.attr("class", function(d) {return "speakerColor_"+d.id;})
			.attr("x", function (d,i){return leftMargin + wStep/2 + i * wStep - rectsWidth/2;} )
			.attr("y", totalH )
			.attr("width", rectsWidth )
			.attr("height", 0 )
			.transition()
				.duration(400)
				.attr("y", function(d,i){return totalH - y_words(d.wordentitycount);} )
				.attr("height", function(d,i){ return y_words(d.wordentitycount);} );
	/////////// TEXT for WORD COUNT
	view_words.selectAll("WordCountText")
		.data(thedata.speakers)
		.enter().append("svg:text")
			.attr("class", "label")
			.attr("x", x_steps )
			.attr("y", function(d,i){ return totalH - y_words(d.wordcount) - 10; } )
			.attr("text-anchor", "middle")
			.text( function(d,i){ return d.wordcount; } );
	/////////// TEXT X LABELS : DISPLAY SPEAKERS NAMES TEXT (xLabels)
	chart.selectAll("SpeakerNames")
		.data(thedata.speakers)
		.enter().append("svg:text")
			.attr("x", x_steps )
			.attr("y", totalH + 20 )
			.attr("text-anchor", "middle")
			.text( function(d,i) {return d.name;} );
						
	///////////////////////////////////////////////////////////////////////////////////////////////////
	//var wordsData = d3.merge( d.map( function(d,i){ return d3.entries(d.tfidf); }))
			
	/////////// CIRCLES for WORDS
	speakerArray = thedata.speakers.map( function(d,i){return d.name;} );
	function getIndexForSpeaker(speakerName) {
		return speakerArray.indexOf(speakerName);
	};
	var x_tfidf = function(d,i) {
		return x_steps( d,getIndexForSpeaker(d.name) );
	};
	var y_tfidfscale = d3.scale.linear()
		.domain([0,maxTfidf])
		.range([0,totalH]);
	var y_tfidf = function(d,i) {
		return totalH - y_tfidfscale(d.tfidf);
	};
	
	/////////// Y LABELS (TFIDF)
	var ytflabels = view_tfidf.selectAll("yTfLabel")
		.data(y_tfidfscale.ticks(6))
		.enter().append("svg:text")
			.attr("fill","#CC6633")
			.attr("x", leftMargin/2 )
			.attr("y", function (d,i){return totalH - y_tfidfscale(d,i);} )
			.attr("text-anchor", "middle")
			.text( function(d,i){return ""+(d*1000).toFixed(3)+"^-3";} );
	/////////// Y Lines (TFIDF)
	var ytflines = view_tfidf.selectAll("yTfLines")
		.data(y_tfidfscale.ticks(6))
		.enter().append("svg:line")
			.attr("y1", function (d,i){return totalH - y_tfidfscale(d,i);} )
			.attr("y2", function (d,i){return totalH - y_tfidfscale(d,i);} )
			.attr("x1", leftMargin - 4)
			.attr("x2", totalW + leftMargin)
			.attr("stroke", "#CC6633")
			.attr("stroke-dasharray","9,5");
/*
	var allwords=null
	var showWordTooltip = function(d,i) {
		//allwords.append("svg:circle"); //'<div id="tooltip"><div class="tipBody">' + d.name + '</div></div>');
		allwords.append("<div>rien</div>");
		console.log("rollover");
	};
	var hideWordTooltip = function(d,i) {
	
	};
*/
	var allwords = view_tfidf.selectAll("Bubbles")
		.data(thedata.words)
		.enter()
			.append("svg:g")
				.on("mouseover", function(d,i) {
						test = d3.select(this).selectAll("text");
						test.attr("class","wordshowed");
					} )
				.on("mouseout", function(d,i) {
						test = d3.select(this).selectAll("text");
						test.attr("class","wordhidden");
					} )
	allwords.append("svg:circle")
		.attr("fill","white")
		.attr("cx", x_tfidf )
		.attr("cy", y_tfidf )
		.attr("r", 4 );
	allwords.append("svg:text")
		.attr("class", "wordhidden")
		.attr("x", x_tfidf )
		.attr("y", function(d,i){return y_tfidf(d,i)-7;} )
		.attr("text-anchor", "middle")
		.text( function(d,i){return d.word;} )
	///////////////////////////////////////////////////////////////////////////////////////////////////
			//.on("mouseover", showWordTooltip )
			//.on("mouseout", hideWordTooltip );

/*
	chart.selectAll("BubblesText")
		.data(thedata.words)
		.enter().append("svg:text")
			.attr("x", x_tfidf )
			.attr("y", y_tfidf )
			.attr("text-anchor", "middle")
			.text( function (d,i){if(i==0) return d.word; else return "";} );
*/
	
	d3.selectAll("#d3initLink").remove();
	initD3TextDefaultValues();
};
////////////////////////////////////////////////////