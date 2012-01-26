////////////////////////////////////////////////////
function buildD3_Attributes(thedata,theId) {
	var vizdiv = d3.select("#"+theId).append("div")
		.attr("class","vizdiv");
	var unikid = "#"+theId+" ";
	
	var spkNames=thedata.spknames;
	var attNames=thedata.attnames;
	var attributes=thedata.attributes;
	var nSpeakers =spkNames.length;
	
	var totalW = 720;
	var chartW = 600;
	var mLeft = 80;
	var mTop = 40;
	var chartH = Math.max(250,nSpeakers*10-mTop+5);
	var chartStep = chartW/attNames.length - 10;
	var totalH = chartH+mTop;
	
	var strokeW = 2;
	var valLabelCol = "#D6D6D6";
	var selValLabelCol = "#FFCC99";//#E8CC80";
	var valRelatedLabelColor = "#FFFFCC";
	var selRelatedColor = "#7490C4";			// DARK BLUE SELECTED
	var vValCol = "#F3F3F3";					// BASE VAL COLOR = GRAY
	var onValCol = "#FFCC99";					// LIGHT ORANGE
	var noteValCol = "#FFCC99";					// for highlighting
	var involvedValCol = "#CBDAF3";				// LIGHT BLUE INVOLVED
	var involvedValColRollover = "#7490C4";		// LIGHT BLUE TRANSITION ROLLOVER
	var involvedValColClick = "#DCAB7E";
	var baseOpacity = 1;
	var maxOpacity = 1;
	var maskOp = 0.2;
	
	var bSpkCircleCol = "#7490C4";
	var bSpkCol = "lightgray";
	var bSpkColSel = "black";
	var onSpkCol = "#FFCC99";
		
	// init array of selected speakers (empty at start)
	var selectedSpk = new Array();
	
	var attlabels = vizdiv.append("div")
		.style("float","none")
		.style("position","relative")
		.style("left",0 )
		.style("top",0 )
	var valuelabels = vizdiv.append("div")
		.style("float","none")
		.style("position","relative")
		.style("left",0 )
		.style("top",0 );
					
	var vis = vizdiv.append("svg:svg")
		.attr("width",totalW)
		.attr("height",totalH)
			.on("click",function(d,i){ deselectAllSpk(); });
		
	vis.append("svg:line")
		.attr("x1",mLeft-10)
		.attr("x2",mLeft-10)
		.attr("y1",0)
		.attr("y2",totalH)
		.attr("stroke","lightgray");
		
	var chart = vis.append("svg:g");
		
	var yScale = d3.scale.linear()
		.domain([0,nSpeakers])
		.range([0,chartH]);
	var xScale = d3.scale.linear()
		.domain([0,attNames.length])
		.range([0,chartW]);
	var cScale = d3.scale.category20()
		.domain([0,nSpeakers]);
	var grayScale = d3.interpolateHsl("#E8E8E8","black");
		
/*
	var opScale = d3.scale.linear()
		.domain([0,nSpeakers-1])
		.range([0.05,1]);
*/
/*
	var drawPath=function(x,y,x1,y1) {
		return "M20 20 L30 30 L100 50 Z";
	}
	chart.append("svg:path")
		.style("fill", "gray")
		.attr("d",drawPath(20,20,50,20));
*/
	var countOccurences = function(arr) {
		var a = [], b = [], prev;
		arr.sort();
		for (var i=0;i<arr.length;i++) {
			if (arr[i]!==prev) {
				a.push(arr[i]);
				b.push(1);
			} else b[b.length-1]++;
			prev = arr[i];
		}
		return [a, b];
	};
	
	
	
	///////////////////////////////////////////////////////////////////////////////////////////////////////// HIGHLIGHT FUNCTIONS
	/*
				ID			CLASS
		RECT	val_id		spk_id,spk_id,...
		SPK		spk_id		val_id,val_id,...
	
	*/
	var highlightSpk = function(spkelem,flag) {
		e = d3.select(spkelem);
		// spk label
		e.attr("fill",function(d,i){return flag ? onSpkCol : bSpkCol;} );
		var classVals = e.attr("class");
		// all val rects
		//d3.selectAll(unikid+".label").style("opacity",function(d,i){return flag ? maskOp : 1;});
		//d3.selectAll(unikid+".val").style("opacity",function(d,i){return flag ? maskOp : 1;});
		// related val rects
		var theVals = classVals.split(" ");
		theVals.pop();
		
		theVals.map( function(u) {
			d3.select(unikid+"#label_"+u).style("background",function(d,i){return flag ? noteValCol : valLabelCol; });
			d3.select(unikid+"#line_"+u).attr("stroke",function(d,i){ return flag ? noteValCol : "transparent"; });
			if(e.attr("sel")!=1){
				d3.select(unikid+"#label_"+u).style("opacity",function(d,i){return flag ? 1 : 0;} );
				d3.select(unikid+"#label_"+u).style("display",function(d,i){return flag ? "inline-block" : "none";} );
				d3.select(unikid+"#"+u).attr("fill",function(d,i){return flag ? involvedValCol : vValCol;});
				var cuy = parseFloat(d3.select(unikid+"#jauge_"+u).attr("height"));
				d3.select(unikid+"#roll_jauge_"+u).attr("y",cuy).transition().attr("height",function(d,i){ return flag ? parseFloat(yScale(1)) : 0; });
			};
			//d3.select(unikid+"#label_"+u).style("opacity",1);
			//d3.select(unikid+"#"+u).style("opacity",1);
		});
		if (!flag) refreshSelected();
	};
	var highlightVal = function(valelem,flag) {
		e = d3.select(valelem);
		// rect
		//e.attr("opacity",function(d,i){return flag ? maxOpacity : baseOpacity;} );
		e.attr("fill",function(d,i){return flag ? onValCol : vValCol;} );
		var valid = e.attr("id");
		// value text
		d3.select(unikid+"#label_"+valid).style("opacity",function(d,i){return flag ? 1 : 0;} );
		d3.select(unikid+"#label_"+valid).style("display",function(d,i){return flag ? "inline-block" : "none";} );
		d3.select(unikid+"#label_"+valid).style("background",function(d,i){return flag ? onValCol : vValCol;} );
		// spk selected special
		var classSpks = e.attr("class").split(" ");
		classSpks.map( function(u) {
			d3.select(unikid+"#"+u).attr("fill",function(d,i){ return flag ? onSpkCol : bSpkCol; });
		});
		if (!flag) refreshSelected();
	};
	var highlightRelatedVals = function(valelem) {
		deselectAllSpk();
		e = d3.select(valelem);
		var valid = e.attr("id");
		var classSpks = e.attr("class").split(" ");
		classSpks.pop(); // remove class "val"
		//console.log("classSpks:"+classSpks);
		for(cs in classSpks){
			//console.log("select:"+classSpks[cs]);
			var spk = d3.select(unikid+"#"+classSpks[cs]);
			selectedSpk.push(spk.attr("id"));
			spk.attr("sel",1);
		}
		refreshSelected();
		showRectsFromSpkArray(classSpks,valid);
	}
	var showRectsFromSpkArray = function(classSpks,curvalid) {
		console.log("showRects,reseting everything");
		// make array of all spk values
		var allValus = new Array();
		for(cs in classSpks) {
			//console.log("spkclass:"+classSpks[cs]);
			var valClasses = d3.select(unikid+"#"+classSpks[cs]).attr("class");
			var curVals = valClasses.split(" ");
			curVals.pop();
			allValus = allValus.concat(curVals);
		}
		//console.log("fromspk:"+classSpks);
		// allValus = [v23,v23,v44,v72, ...]
		// countOccurences() returns = [ [v23,v44,...] [2,1,...] ]
		var counts = countOccurences(allValus);
		//console.log("counts:"+counts);
		// all val labels off
		d3.selectAll(unikid+".label").style("display","none");
		d3.selectAll(unikid+".line").attr("stroke","transparent");
		d3.selectAll(unikid+".jauge").attr("height",0);
		d3.selectAll(unikid+".roll_jauge").attr("y",0).attr("height",0);
		// curent selected
		if(valid) {
			d3.select(unikid+"#label_"+valid).style("display","inline-block");
			d3.select(unikid+"#"+valid).attr("fill",involvedValColClick);
		}
		// looking at EVERY val
		allVals = d3.selectAll(unikid+".val")[0];
		for(v=0;v<allVals.length;v++) {
			var valid = d3.select(allVals[v]).attr("id");
			var flag = counts[0].indexOf(valid)!=-1;
			
			if(flag) {
				var nS = counts[1][counts[0].indexOf(valid)];
				d3.select(unikid+"#jauge_"+valid).attr("height",yScale(nS)-strokeW);
			}
			else d3.select(unikid+"#jauge_"+valid).attr("height",0);
				
			d3.select(unikid+"#label_"+valid).style("opacity",function(d,i){return flag ? 1 : 0;} );
			d3.select(unikid+"#label_"+valid).style("display",function(d,i){return flag ? "inline-block" : "none";} );
			d3.select(unikid+"#label_"+valid).style("background",function(d,i){return flag ? valLabelCol : valLabelCol;} );
			d3.select(unikid+"#"+valid).attr("fill",function(d,i){return flag ? involvedValCol : vValCol;});
			d3.select(unikid+"#line_"+valid).attr("stroke",function(d,i){ return flag ? valLabelCol : "transparent"; });		
		}		
/*
		for(v in counts[0]) {
			var valid = counts[0][v]
			if (valid != curvalid) {
				console.log("value"+valid);
				// show val label
				d3.select(unikid+"#label_"+valid).style("display","inline-block");
				// also color for whole val rect
				d3.select(unikid+"#"+valid).attr("fill",involvedValCol);
				//line
				d3.select(unikid+"#line_"+valid).attr("stroke",valLabelCol);
				// fill jauge rect
				var nS = counts[1][v]; // to set new height
				d3.select(unikid+"#jauge_"+valid).transition().attr("height",yScale(nS)-strokeW);
				
				d3.select(unikid+"#label_"+valid).transition().duration(500).style("opacity",1 );
				d3.select(unikid+"#label_"+valid).style("background",valLabelCol );			
				//var cuy = parseFloat(d3.select(unikid+"#jauge_"+u).attr("height"));
				//d3.select(unikid+"#roll_jauge_"+u).attr("y",cuy).transition().attr("height",function(d,i){ return flag ? parseFloat(yScale(1)) : 0; });
			
			}
		}
*/
	};
	//////////////////////////////////////////////// CLICK
	var refreshSelected = function(){
		console.log("refreshSelected");
		// no labels
		d3.selectAll(unikid+".label").style("display","none");
		// base color for every rect
		d3.selectAll(unikid+".val").attr("fill",vValCol);
		d3.selectAll(unikid+".spk").attr("fill",function(d,i){ return d3.select(this).attr("sel")==1 ? bSpkCol : bSpkCol ; });
		// crosses
		d3.selectAll(unikid+".cross").style("display","none");
		for(sid in selectedSpk) {
			d3.selectAll(unikid+"#cross_"+selectedSpk[sid]).style("display","block");
		}
		// for each selectedSpk
		showRectsFromSpkArray(selectedSpk,-1); // -1 because we dont want to highlight special val
	};
	var clickOnSpk = function(spkelem){
		var sp = d3.select(spkelem);
		var spid = sp.attr("id");
		var pos = selectedSpk.indexOf(spid);
		if(pos==-1) selectedSpk.push(spid);
		else selectedSpk.splice(pos,1);
		sp.attr("sel",pos==-1 ? 1 : 0);
		refreshSelected();
	};
	var deselectAllSpk = function() {
		selectedSpk = new Array();
		d3.selectAll(unikid+".cross").style("display","none");
		d3.selectAll(unikid+".spk").attr("sel",0);
		refreshSelected();
	};
	////////////////////////////////////////////////////////////////////////////////// SPEAKERS
	var spks = chart.selectAll("theSpks")
		.data(spkNames)
		.enter().append("svg:g");
		
	spks.append("svg:text")
		.attr("id",function(d,i){return "spk_"+d.id;} )
		.attr("class",function(d,i){ return d.values.map(function(w){return "val_"+w;}).join(" ")+" spk"; })
		.attr("sel",0)
		.attr("y",function(d,i){return 10+i*10;} )
		.attr("x",10 )
		.attr("text-anchor","left")
		.attr("fill",bSpkCol)
		//.attr("opacity",bSpkCol)
		.text(function(d,i){return d.name;} )
		.style("cursor","pointer")
			.on("mouseover",function(d,i){highlightSpk(this,true);} )
			.on("mouseout",function(d,i){highlightSpk(this,false);} )
			.on("click",function(d,i){ clickOnSpk(this);d3.event.stopPropagation(); });
	spks.append("svg:circle")
		.attr("id",function(d,i){return "cross_spk_"+d.id;} )
		.attr("class","cross")
		.attr("cx",3)
		.attr("cy",function(d,i){return 6+i*10;})
		.attr("r",3)
		.style("display","none")
		.attr("fill",bSpkCircleCol);
		
	///////////////////////////////////////////////////////////////////////////////// ATTRIBUTES
	var atts = chart.selectAll("theAtts")
		.data(attributes)
		.enter().append("svg:g");
	////////////////////////////////// for each attributetype				
	atts.each(function(q,j) {
		//console.log("oui"+q+"++"+j);
		var attx = mLeft+xScale(j);		
		var att = d3.select(this).append("svg:g");
		
		//////////////// attributetype label (on top)
		attlabels.append("div")
			.style("display","inline-block")
			//.style("float","none")
			.style("position","absolute")
			.style("width",chartStep)
			.style("left",attx )
			.style("top",0 )
			//.style("background","lightgray")
			.style("color","black")
			.style("font-size","0.8em")
			.style("text-align","center")
			.text(attNames[j].name);
		
		/////////////// sort array values based on...
		valuesArray = q;
		if(attNames[j].name=='Age')
			valuesArray.sort(function(a,b) {
				var m=parseInt(a.name);
				var n=parseInt(b.name);
				return (m>n);
			});
		else
			valuesArray.sort(function(a,b) {
				var m=a.speakers.length;
				var n=b.speakers.length;
				return (m<n);
			});
			
		//////////////// add each value rect
		var theVals	= att.selectAll("theVals")
			.data(valuesArray)
			.enter().append("svg:g");
					
		var rects = theVals.append("svg:g")
			.attr("transform","translate(0,"+totalH+")scale(1,-1)");
		
		var avalue = rects.append("svg:g")
			.attr("transform",function(d,i){
				var cury=0;
				for(k=0;k<i;k++) {
					cury+=q[k].speakers.length;
				}
				return "translate(0,"+yScale(cury)+")";
			});
			
		//////////////////////////////////////// EACH VALUE RECT
		avalue.append("svg:rect")
			.attr("label",function(d,i) {return d.name;} )
			.attr("id",function(d,i){return "val_"+d.id;})
			.attr("class",function(d,i){ return d.speakers.map(function(w){return "spk_"+w;}).join(" ")+" val"; })
			.attr("x",attx )
			.attr("y",0)
			.attr("width",chartStep )
			.attr("height",function(d,i){ return yScale(d.speakers.length); })
			.attr("stroke","white")
			.attr("stroke-width",strokeW)
			.attr("fill",vValCol)//function(d,i){return cScale(valuesArray.length-i);} )
			.attr("opacity",baseOpacity)
				.on("click",function(d,i){highlightRelatedVals(this);d3.event.stopPropagation();} )
				.on("mouseover",function(d,i){highlightVal(this,true);} )
				.on("mouseout",function(d,i){highlightVal(this,false);} );

		//////////////////////////////////////// SELECTED JAUGE RECT
		avalue.append("svg:rect")
			.attr("id",function(d,i){return "jauge_val_"+d.id;})
			.attr("class","jauge")
			.attr("x",attx+strokeW/2)
			.attr("y",strokeW/2)
			.attr("width",chartStep-strokeW )
			.attr("height",0)
			.attr("fill",selRelatedColor)
			.attr("opacity",baseOpacity);
			
		//////////////////////////////////////// ROLLOVER JAUGE RECT
		avalue.append("svg:rect")
			.attr("id",function(d,i){return "roll_jauge_val_"+d.id;})
			.attr("class","roll_jauge")
			.attr("x",attx+strokeW/2)
			.attr("y",strokeW/2)
			.attr("width",chartStep-strokeW )
			.attr("height",0)
			.attr("fill",involvedValColRollover)
			.attr("opacity",baseOpacity);	
					
		//////////////////////////////////////// LEFT LINE
		avalue.append("svg:line")
			.attr("id",function(d,i){return "line_val_"+d.id;})
			.attr("class","line")
			.attr("x1",attx)
			.attr("x2",attx)
			.attr("y1",1)
			.attr("y2",function(d,i){ return yScale(d.speakers.length)+2; })
			.attr("stroke-width",3)
			.attr("stroke","transparent");
		
		//////////////////////////////////////// TOP LABEL FOR EACH VAL RECT
		avalue.each( function(g,y) {
			// get posy
			var cury=0;
			for(k=0;k<y+1;k++) {
				cury+=q[k].speakers.length;
			} 
			var posy = totalH-yScale(cury);
			var valLab = valuelabels.append("div")
				.attr("id",function(dd,ii){return "label_val_"+g.id;} )
				.attr("class","label")
				.style("display","none")
				.style("position","absolute")
				.style("width",chartStep+1)
				.style("left",attx-1 )
				.style("background",valLabelCol)
				.style("color","black")
				.style("font-size","0.8em")
				.style("text-align","center")
				.text(g.name);
			// NB: using jquery 'cause unable to get calculated size with d3 (?)
			var curH = $(unikid+"#label_val_"+g.id).height();
			d3.select(unikid+"#label_val_"+g.id).style("top",posy-curH);
		});

/*
		theVals.append("svg:text")
			.attr("id",function(d,i){return "label_val_"+d.id;} )
			.attr("x",mLeft+xScale(j)+chartStep/2 )
			//.attr("y",mTop+chartH+15 )
			.attr("y",function(d,i){
				var cury=0;
				for(k=0;k<i;k++) {
					cury+=q[k].speakers.length;
				} 
				return mTop+yScale(cury)-5;
			})
			.attr("font-size",9)
			.attr("fill","gray")
			.attr("background-color","white")
			.attr("display","none" )
			.text(function(d,i){return d.name;} )
			.attr("text-anchor","middle");
*/

	});
};
////////////////////////////////////////////////////