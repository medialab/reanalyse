////////////////////////////////////////////////////
function buildD3_Overview(data,theId,param) {
	var unik = "#"+theId;
	var vizdiv = d3.select(unik).append("div")
		.attr("class","vizdiv");
	
	links = data['links'];
	nLinks = links.length;
	
	//////////////////////////////////////// update spk weights from stats dict, if present
	var mode='document';
	if(param) {
		var stats=param.stats;
		for(k in links) {
			var sid = links[k].spk.id;
			if(sid in stats) links[k].spk.weight = stats[sid] ;
			else links[k].spk.weight = 0;
			//console.log("updated weight:"+links[k].spk.label+":"+links[k].spk.weight);
		}
		mode=param.mode;
		//console.log(unik+":param dic received and mode set to:"+mode);
	}
	else console.log(unik+":no param dic given to update spk weights");
	
	//////////////////////////////////////// SELECTION
	var selectedSpk = new Array();
	for(k in links)
		if(links[k].spk.weight==0)
			selectedSpk[links[k].spk.id]=false;
		else
			selectedSpk[links[k].spk.id]=true;
	
	var maxSpkDoc = links.length;
/*
	for(l in links) {
		maxSpkDoc = Math.max(speakers.length,textes.length);
	}
*/
	var baseOpacity = 1;
	var selOpacity = 0.9;
	var overOpacity = 1;
	///////////
	var leftMargin=0;
	var topMargin=10;
	var totalW=150;
	var weightLabelFontSize=9;
	var zeroStrokeWidth=4;
	var selStrokeWidth=4;
	var spaceForEach=3;
	var totalH= maxSpkDoc*spaceForEach + 2*topMargin;

	var bezierDec=25;
	var bezierMargin=2;

	////////// SPK WEIGHT
	var xDoc = leftMargin;
	var minXSpk = 60;
	var xSpk = 70;
	var maxWeightSpeaker = d3.max(links,function(d,i){return d.spk.weight;});
	var minWeightSpeaker = d3.min(links,function(d,i){return d.spk.weight==0 ? maxWeightSpeaker:d.spk.weight;});
	//console.log("maxWeightSpeaker:"+maxWeightSpeaker);
	console.log("minWeightSpeaker:"+minWeightSpeaker);
	
	//var labelSelSize=15;
	var spkScaleX=d3.scale.linear()
		.domain([0,maxWeightSpeaker])
		.range([minXSpk,xSpk]);
	var labelScale=d3.scale.linear()
		.domain([0,maxWeightSpeaker])
		.range([7,9]);
	var labelSelScale=d3.scale.linear()
		.domain([0,maxWeightSpeaker])
		.range([10,12]);
	
	
	/////////// SORT BUTTONS
	var sortdiv = vizdiv.append("div");
	sortdiv.append("span")
		.text("sort using: ");
	sortdiv.append("a")
		.style("cursor","pointer")
		.text("involved")
		.on("click", function() { mode='weight'; sortLinks(); });
	sortdiv.append("span").text(" | ");
	sortdiv.append("a")
		.style("cursor","pointer")
		.text("docs")
		.on("click", function() { mode='document'; sortLinks(); });

	/////////// GENERAL CHART		
	var chart = vizdiv.append("svg:svg")
		.attr("width", totalW)
		.attr("height", totalH);
				
	/////////////////////////////////////////////////
	
	// then test sorting by nameofspk/weight/document(=default)/...
	
	/////////////////////////////////////////////////
/*
	var tStep=totalH/maxTextes;
	var sStep=totalH/maxSpeakers;
	var dcons = totalH - topMargin ; 
	var dfact = totalH - 2*topMargin;
	var yTextes = function(d,i) {
		return dcons - tStep/2 - i*dfact/nLinks;
	}
	var ySpeakers = function(d,i) {
		return dcons - sStep/2 - i*dfact/nLinks;
	}
*/
		
	var getSpkOpacity = function(d,i){
		return selectedSpk[d.spk.id] ? selOpacity : baseOpacity ;
	};
	var getSpkLabelFill = function(d,i){
		return selectedSpk[d.spk.id] ? "black" : "lightgray" ;
	}
	///////////////////////////////////////////////////////////////////////////// LINKS
	var buildList = function() {
		chart.selectAll(".all").remove();
		var subchart = chart.append("svg:g").attr("class","all");
		var thelinks = subchart.selectAll("alinks")
			.data(links)
			.enter().append("svg:g");
		
		// PATH LINK
		thelinks.append("svg:path")
			.attr("class",function(d,i){return "link doc_"+d.doc.id+" spk_"+d.spk.id;})
			.attr("stroke",function(d,i){return d.spk.weight==0 ? "#B0B0B0"  : "red";})
			.attr("stroke-width",function(d,i){return d.spk.weight==0 ? zeroStrokeWidth:selStrokeWidth;})
			.attr("fill","none")
			.style("opacity",getSpkOpacity)
			.attr("d", function(d,i) {
				u = getY(d,i);
				// from
				var xT = xDoc+bezierMargin;
				var yT = u[0];
				// to
				var xS = spkScaleX(d.spk.weight)-bezierMargin;
				var yS = u[1];
				return "M "+xT+" "+yT+" C "+(xT+bezierDec)+" "+yT+" "+(xS-bezierDec)+" "+yS+" "+xS+" "+yS;
			})
			.on("mouseover",function(d,i){highlight(d.spk.id,true);})
			.on("mouseout",function(d,i){highlight(d.spk.id,false);});
		
		// SPK LABEL	
		thelinks.append("svg:text")
			.attr("class",function(d,i){return "label spk_"+d.spk.id;})
			.style("opacity",0)
			//.attr("x", function(d,i){return 3+xSpk;} )
			.attr("x", function(d,i){return 5+spkScaleX(d.spk.weight)-bezierMargin;} )
			.attr("y", function(d,i){return 4+getY(d,i)[1];} )
			.attr("fill",getSpkLabelFill)
			.attr("text-anchor", "left")
			.style("cursor","pointer")
			.attr("font-size",function(d,i){return labelScale(d.spk.weight);})
			.text(function(d,i){return d.spk.label;})
				.on("mouseover",function(d,i){highlight(d.spk.id,true);})
				.on("mouseout",function(d,i){highlight(d.spk.id,false);});
		
		// WEIGHT LABEL
		thelinks.append("svg:text")
			.attr("class",function(d,i){return "weight spk_"+d.spk.id;})
			.style("opacity",0)
			.attr("x", function(d,i){return totalW-2;} )
			.attr("y", function(d,i){return 4+getY(d,i)[1];} )
			.attr("fill",getSpkLabelFill)
			.attr("text-anchor", "end")
			.style("cursor","pointer")
			.attr("font-size",weightLabelFontSize)
			.text(function(d,i){return d.spk.weight;})
				.on("mouseover",function(d,i){highlight(d.spk.id,true);})
				.on("mouseout",function(d,i){highlight(d.spk.id,false);});

		// FIXED WEIGHT LABEL for max/min values
		if(maxWeightSpeaker==0) {
			var minY=totalH-topMargin;
			var minVal=0;
		} else {
			var minY=0;
			for(k in links) {
				if(links[nLinks-k-1].spk.weight!=0) {
					minY = 4+parseInt(getY(0,nLinks-k-1));
					break;
				}
			}
			var minVal=minWeightSpeaker;
		}
		var fixedWeights = [[4+parseInt(getY(0,0)),maxWeightSpeaker],[minY,minVal]];
		subchart.selectAll("fixedlabels")
			.data(fixedWeights)
			.enter().append("svg:text")
				.attr("class","fixedlabel")
				.style("opacity",1)
				.attr("x",totalW-2)
				.attr("y",function(d,i){return d[0];})
				.attr("fill","black")
				.attr("text-anchor", "end")
				.style("cursor","pointer")
				.attr("font-size",weightLabelFontSize)
				.text(function(d,i){return d[1];});
	}
	
	///////////////////////////////////////////////////////////////////////////// FUNCTIONS
	var highlight = function(spkid,flag) {
		d3.selectAll(unik+" .link").style("opacity",function(d,i){return flag ? 0.1 : getSpkOpacity(d,i) ;});
		d3.select(unik+" .link.spk_"+spkid).style("opacity",function(d,i){return flag ? 1 : getSpkOpacity(d,i) ;});
		d3.select(unik+" .weight.spk_"+spkid).style("opacity",function(d,i){return flag ? 1 : 0 ;});
		d3.select(unik+" .label.spk_"+spkid).style("opacity",function(d,i){return flag ? 1 : 0 ;});
		d3.select(unik+" .label.spk_"+spkid).attr("font-size",function(d,i){return flag ? labelSelScale(d.spk.weight) : labelScale(d.spk.weight) ;})
	};
	var sortLinks = function() {
		//console.log("sorting using:"+mode);
		if(mode=='weight') {
			// here we have to bring near speakers sharing a doc in each level, to avoid "diagonal-long" lines
			links.sort(function(a,b) {
				return b.spk.weight-a.spk.weight;
				// DEPRECATED, cause now we just sort and distinguish each spk-doc (simple lines)
/*				
				var difw = b.spk.weight-a.spk.weight;
				var difdid = b.doc.id-a.doc.id;
				var difndoc = b.ndoc-a.ndoc;
				if(difw!=0) return difw;
				else {
					if(difndoc!=0) return difndoc;
					else return difdid;
				}
*/
			});
			buildList();
		}
		if(mode=='document') {
			// if multiple spk per doc, no pb, they will be near to each other
			links.sort(function(a,b) {return b.doc.id-a.doc.id;});
			buildList();
		}
	};
	var simplesc = d3.scale.linear().domain([0,links.length-1]).range([topMargin,totalH-topMargin]);
	var getY=function(d,i) {
		// all links parallell
		if(mode=='weight') {
			return [simplesc(i),simplesc(i)];
		}
		// taking care of joins if doc with multiple spk
		else {
			var iDoc=new Array();
			var iSpk=new Array();
			var cDoc=0;
			var cSpk=0;
			for(k in links){
				l=links[k];
				if(k==0) {
					iDoc[l.doc.id]=0;
					iSpk[l.spk.id]=0;
				} else {
					lp=links[k-1];
					if(l.doc.id!=lp.doc.id) cDoc+=1;
					if(l.spk.id!=lp.spk.id) cSpk+=1;
					iDoc[l.doc.id]=cDoc;
					iSpk[l.spk.id]=cSpk;
				}
			};
			var idDocScale=d3.scale.linear()
				.domain([0,cDoc])
				.range([topMargin,totalH-topMargin]);
			var idSpkScale=d3.scale.linear()
				.domain([0,cSpk])
				.range([topMargin,totalH-topMargin]);
			return [idDocScale(iDoc[d.doc.id]),idSpkScale(iSpk[d.spk.id])];
		}
	};
	
	sortLinks();
	buildList();
};
////////////////////////////////////////////////////






















/*
	///////////////////////////////////////////////////////////////////////////// TEXTES
	var tLabels = chart.selectAll("tLabel")
		.data(textes)
		.enter().append("svg:text")
			.attr("class",function(d,i){return "doc doc_"+d.id;})
			.attr("weight",function(d,i){return d.weight;})
			.attr("x", leftMargin )
			.attr("y", function(d,i){return 2+yTextes(d,i);} )
			.attr("text-anchor", "end")
			.attr("font-size",2)
			.text( function(d,i){return d.label;} );
			
	///////////////////////////////////////////////////////////////////////////// SPEAKERS
	var sLabels = chart.selectAll("sLabel")
		.data(speakers)
		.enter().append("svg:text")
			.attr("class",function(d,i){return "spk spk_"+d.id;})
			.attr("weight",function(d,i){return d.weight;})
			.attr("x",function(d,i){return spkScaleX(d.weight);})
			.attr("y", function(d,i){return 2+ySpeakers(d,i);} )
			.attr("text-anchor", "left")
			.attr("font-size",2)
			.text( function(d,i){return d.label;} );
	sLabels.append("svg:circle")
		.attr("r", 4.5);
*/








////////////////////////////////////////////////////
function buildD3_Overview_Graph(data,theId) {
	console.log("try build");
	var totalW = 190;
	var totalH = 190;
	var nSpkS = 2;
	var nDocS = 3;
	
	var vis = d3.select("#"+theId).append("svg:svg")
		.attr("width", totalW)
		.attr("height", totalH);
	
	var force = d3.layout.force()
		.charge(-5)
		.linkDistance(1+Math.random()*20)
		.nodes(data.nodes)
		.links(data.edges)
		.size([totalW, totalH])
		.start();
	
	var spkColor = function(i) {
		return Math.random()<0.5 ? "red" : "lightgray";
	}
	var docColor = function(i) {
		return Math.random()<0.5 ? "red" : "lightgray";
	}
	////////////////////////////////////////// Graph		
/*
	var edge = vis.selectAll("line.edge")
		.data(data.edges)
		.enter().append("svg:line")
			.attr("stroke","gray")
			//.style("stroke-width", function(d) { return Math.sqrt(d.value); })
			.style("opacity",0.1)
			.attr("class", function(d) { return "edge edgeid_"+d.source.id+" edgeid_"+d.target.id; })
			.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
*/
	
	var node = vis.selectAll("circle.node")
		.data(data.nodes)
		.enter().append("svg:circle")
			.attr("cx", function(d) { return d.x;} )
			.attr("cy", function(d) { return d.y;} )
			.attr("r", function(d) { return d.category=='Speaker' ? nSpkS : nDocS ; })
			.style("fill", function(d,i) { return d.category=='Speaker' ? spkColor(i) : "white" ; })
			.style("stroke", function(d,i) { return d.category=='Speaker' ? "white" : docColor(i) ; })
			.attr("id", function(d) { return d.id ; })
			.call(force.drag);
			
/*
	var labels = vis.selectAll("textlabels")
		.data(data.nodes)
		.enter().append("svg:text")
			.attr("class","textlabs")
			//.style("display","none")
			.style("opacity", 0.1)
			.attr("x", function(d) {return d.x+10 ; })
			.attr("y", function(d) {return d.y+5; })
			.attr("fill","black")
			.attr("text-anchor","left")
			.text( function(d) {return d.label;} );
*/
			
	force.on("tick", function() {
/*
		edge.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
*/
			
		node.attr("cx", function(d) { return d.x;} )
			.attr("cy", function(d) { return d.y;} )
	});
};
