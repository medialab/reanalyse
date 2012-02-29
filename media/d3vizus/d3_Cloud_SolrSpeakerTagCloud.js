/////////////////////////////////////////////////////////////////////
function buildD3_Cloud_SolrSpeakerTagCloud(data,theId) {
	var vizdiv = d3.select("#"+theId).append("div")
		.attr("class","vizdiv");
	var unik = "#"+theId;

	var thewordlist = null;
	
	var curMode = 'vizlist';
	
	var highlightColor = "#FFFFCC";
	var margy = 30;
	var decLeft = 210;
	var decy = 15;
	var totalW = 720;
	var totalH = decy*data.words.length + 50;
	
	var maxSpeaker = data.speakers.length;
	//console.log("maxSpeaker:"+maxSpeaker);
	var thespeakerids = new Array();
	for (u in data.speakers) {
		thespeakerids.push(data.speakers[u][1]);
	}
	////////////////////////////////////////////////////////////// SCALE VALUES
	var minCount = d3.min(data.words, function(d) { return d.count;});
	var maxCount = d3.max(data.words, function(d) { return d.count;});
	var minColor = d3.min(data.words, function(d) { return d.tf;});
	var maxColor = d3.max(data.words, function(d) { return d.tf;});
	if(minColor==maxColor) {
		console.log("minColor=maxColor ! all words will be gray !");
	}
	// SCALE HORIZONTAL for Speakers
	var scalespeakers = d3.scale.linear()
		.domain([0,maxSpeaker])
		.range([decLeft,totalW]);
	var scalcount = d3.scale.linear()
		.domain([minCount,maxCount])
		.range([0.9,1.5]);
	var scalcolor = d3.scale.sqrt()
		.domain([minColor,maxColor])
		.range([0,1]);
	var color = d3.interpolateRgb("#A8A8A8", "#000000");
	
	function getColor(d) {
		return minColor==maxColor ? "gray" : color(scalcolor(d.tf)) ;
	};	
	
	// todo: find a better way than this scrapy one
	var stepx = parseInt(scalespeakers(2))-parseInt(scalespeakers(1));
	
	//////////////////////////////////////////////////////////// MENU ACTIONS
/*
	vizdiv.append("a")
		.style("cursor","pointer")
		.text("switch view")
		.on("click", rebuild);
	vizdiv.append("span").text(" | ");
*/
	vizdiv.append("span")
		.text("sort using: ");
	vizdiv.append("a")
		.style("cursor","pointer")
		.text("alphabet")
		.on("click", function() { sortClick('alphabet'); });
	vizdiv.append("span").text(" | ");
	vizdiv.append("a")
		.style("cursor","pointer")
		.text("tfidf")
		.on("click", function() { sortClick('tfidf'); });
	vizdiv.append("span").text(" | ");
	vizdiv.append("a")
		.style("cursor","pointer")
		.text("termfrequency")
		.on("click", function() { sortClick('tn'); });
	
	vizdiv.on("mouseout",deHighlightWords);
	
	function sortClick(typ) {
		if (curMode=='viztable') buildTable(typ);
		else sortBy(typ);
	}
	function sortBy(typ) {
		if(typ=='tn')
			thewordlist.sort(function(a,b) { return (a.tn > b.tn) ? -1 : (a.tn < b.tn) ? 1 : 0; });
		if(typ=='tfidf')
			thewordlist.sort(function(a,b) { return (a.count > b.count) ? -1 : (a.count < b.count) ? 1 : 0; });
		if(typ=='alphabet')
			thewordlist.sort(function(a,b) { return (a.word < b.word) ? -1 : (a.word > b.word) ? 1 : 0; });
	};	


	//////////////////////////////////////////////////////////// HIGHLIGHT SIMILAR WORDS
	function isSimilar(word1,word2) {
		var found = 0;
		if(word2.indexOf(word1)!=-1) found=5;
		else {
			var morc = word1.split(" ");
			for (p in morc) {
				if (word2.indexOf(morc[p])!=-1)
					found+=morc[p].length;
			}
		}
		return found>4;
	}
	function deHighlightWords() {
		thewordlist.selectAll("a")
			.style("background-color","transparent")
	}
	function highlightWords(d,i) {
		if (curMode=='vizlist') {
			thewordlist.selectAll("a")
				.style("background-color","transparent")
				.filter( function(g,k) { // filter only similar words
					return isSimilar(d.word,g.word) ? this : null ;
				})
				.style("background-color",highlightColor);
		}
		else {
			thewordlist.selectAll("rect")
				.attr("fill","transparent")
				.filter( function(g,k) { // filter only similar words
					return isSimilar(d.word,g.word) ? this : null ;
				})
				.attr("fill",highlightColor);
		}
	};


	//////////////////////////////////////////////////////////////////////////////////////////////////////// BUILD
	buildList();
	curMode = "vizlist";
	//buildTable();
	//curMode = "viztable";
	
	function rebuild() {
		//////////////////////// FIRST WAY : ul+li
		if (curMode=='viztable') {		
			//vizdiv.select(".viztable").style("display","none");
			//if(vizlist==null) buildList();
			//vizdiv.select(".vizlist").style("display","visible");
			buildList('tfidf');
		}
		////////////////////////  SECOND WAY : one SVG
		else {
			//vizdiv.select(".vizlist").style("display","none");
			//if(viztable==null) buildTable();
			//vizdiv.select(".viztable").style("display","visible");
			buildTable('tfidf');
		}
	};
	/////////////////////////////////////////////////////////////////////////////	
	function buildList(sorttype) {
		vizdiv.select(".viztable").remove();
		curMode='vizlist';

		var list = vizdiv.append("ul").attr("class","vizlist viz_Cloud");
	
		thewordlist = list.selectAll("li")
			.data(data.words)
			.enter().append("li");
		
		sortBy(sorttype);
		
		thewordlist.append("a")
			.attr("rel","tooltip")
			.attr("title", function(d,i) {return "count="+d.count+" tfidf="+d.tfidf+" df="+d.df+" tf="+d.tf+" dn="+d.dn+" tn="+d.tn;})
			.style("color", function(d,i) {return getColor(d);})
			.style("font-size", function(d,i) {return scalcount(d.count)+"em";})
			.text( function(d,i) {return d.word;})
			.on("mouseover", function(d,i) {highlightWords(d,i);});
			
		thewordlist.append("span")
			//.style("color","#E8E8E8")
			.style("margin-left","10px");
			//.text("e");
	};
	//////////////////////////////////////////////////////////////////////////////
	function buildTable(sorttype) {
		vizdiv.select(".vizlist").remove();
		vizdiv.select(".viztable").remove();
		curMode='viztable';
		
		var svg = vizdiv.append("svg:svg")
			.attr("class","viztable")
			.attr("width","100%")
			.attr("height",totalH);
			//.style("background","lightgray");
			
		thewordlist = svg.selectAll("list")
			.data(data.words)
			.enter().append("svg:g");
		
		sortBy(sorttype);
		
		// Horizontal rects
		thewordlist.append("svg:rect")
			.attr("x",0)
			.attr("y",function(d,i) {return margy+decy*i;})
			.attr("width",totalW)
			.attr("height",decy)
			.attr("fill", "transparent") //function(d,i) {return i%2==0 ? "#D8D8D8" : "white";} )
			//.style("opacity",0.2)
			.on("mouseover",function(d,i) { highlightWords(d,i); });
		
		// THE WORDS on the left !				
		thewordlist.append("svg:text")
			//.attr("title", function(d,i) {return "count="+d.count+" tfidf="+d.tfidf+" df="+d.df+" tf="+d.tf+" dn="+d.dn+" tn="+d.tn;})
			.attr("x",5)
			.attr("y",function(d,i) {return margy+decy*(i+1)-2;})
			.style("color", function(d,i) {return getColor(d);})
			.style("font-size", function(d,i) {return scalcount(d.count)+"em";})
			.style("cursor","pointer")
			.text( function(d,i) {return d.tn+" "+d.word;})
			.on("mouseover",function(d,i) { highlightWords(d,i); });
			
		// Horizontal lines
		thewordlist.append("svg:line")
			.attr("x1",decLeft )
			.attr("y1",function(d,i) {return margy+decy*i;})
			.attr("x2",totalW )
			.attr("y2",function(d,i) {return margy+decy*i;})
			.attr("stroke","#E8E8E8");	
				
		svg.selectAll("vlines")
			.data(scalespeakers.ticks(data.speakers.length))
			.enter().append("svg:line")
				.attr("x1",function(d,i) {return scalespeakers(d);} )
				.attr("y1",0)
				.attr("x2",function(d,i) {return scalespeakers(d);} )
				.attr("y2",totalH)
				.attr("stroke","#E8E8E8");
		svg.selectAll("vrects")
			.data(data.speakers)
			.enter().append("svg:rect")
				.attr("x",function(d,i) {return scalespeakers(i);} )
				.attr("y",0)
				.attr("width",stepx )
				.attr("height",totalH)
				.attr("class", function(d) {return "speakerColor_"+d[1];} )
				.style("opacity",0.2);

		// Speakers (columns) Labels & simil score
		svg.selectAll("speakerLabels")
			.data(data.speakers)
			.enter().append("svg:text")
				.attr("x",function(d,i) {return 5+scalespeakers(i);} )
				.attr("y",15)
				.text( function(d,i) {return d[2]+" ("+d[0].toFixed(2)+")";});
							
		thewordlist.each( function(d,i) {
			var anch = d3.select(this).append("svg:g");
			var theSpeakers	= anch.selectAll("thespks")
				.data(d.speakers)
				.enter().append("svg:g");
				
/*
			theSpeakers.append("svg:rect")
				.attr("x",function(g,k) { return scalespeakers(thespeakerids.indexOf(g.id)); })
				.attr("y",function(g,k) {return margy+decy*(i-1);})
				.attr("width",stepx)
				.attr("height",decy)
				.attr("class", function(g) {return "speakerColor_"+g.id;} );
*/

/*
			theSpeakers.append("svg:circle")
				.attr("cx",function(g,k) { return parseFloat(scalespeakers(thespeakerids.indexOf(g.id)))+stepx/2; })
				.attr("cy",function(g,k) {return margy+decy*i-decy/2;})
				.attr("r", function(g,k) {return 3+g.tn*3;})
				.attr("stroke","lightgray")
				.style("opacity",0.6)
				.attr("class", function(g) {return "speakerColor_"+g.id;} );
*/
			// Simil Speakers tf in correspondant cells		
			theSpeakers.append("svg:text")
				.attr("x",function(g,k) { return stepx/2+scalespeakers(thespeakerids.indexOf(parseInt(g.id))); } )
				.attr("y",function(g,k) {return margy+decy*(i+1)-3;})
				.attr("text-anchor","middle")
				.text(function(g,k) { return g.tn; });
		});
	}
}


