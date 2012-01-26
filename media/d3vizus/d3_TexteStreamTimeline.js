////////////////////////////////////////////////////
function buildD3_TexteStreamTimeline(thedata,theId) {
	var unik = "#"+theId;
	var vizdiv = d3.select(unik).append("div")
		.attr("class","vizdiv")
		.style("position","relative"); // relative to allow sub-div "absolute" to be positionned
			
	var textPartsRefreshMode = false;
	if(typeof(getVerbatimParts)=='function') textPartsRefreshMode=true;
	
	//var ww = d3.select("#"+theId).style("width");
	//console.log("width is:"+ww);
	
	////////////////////////////////////////////////////////////////////////////////////// FADE AND HIGHLIGHT
	var fadeMinSpk = 0.1;
	var fadeMinPar = 0.05;
	var fadePar = 0.5;
	
	function highlightSpk(flag) {
		return function(g, i) {
			vis.selectAll(unik+" .spk_graph").style("opacity", flag ? 1:fadeMinSpk);
			vis.select(unik+" .spk_graph_"+i).style("opacity", 1);
			vis.selectAll(unik+" .spk_rect").style("opacity", flag ? 1:fadeMinSpk);
			vis.select(unik+" .spk_rect_"+i).style("opacity", 1);
			vis.selectAll(unik+" .spk_label").attr("fill",flag ? "gray":"lightgray");
			vis.select(unik+" .spk_label_"+i).attr("fill","gray");
		};
	}
	///////////// Parvbl flags to show/hide
	var displayParvbBool = new Array();
	for (i in thedata.par_layers) {
		displayParvbBool.push(true);
	}
	var showHideAllParaverbal = function(flag) {
		for(i in thedata.par_layers)
			if(displayParvbBool[i] || !flag) showHideParaverbal(i,flag);
	};
	var showHideParaverbal = function(i,flag) {
		//displayParvbBool[i] = !displayParvbBool[i];
		//console.log("clicked:"+i+":"+displayParvbBool[i]);
		//visGraph.selectAll(".par_graph_"+i).attr("display", flag ? "visible":"none");
		visGraph.selectAll(".par_graph_"+i).attr("opacity", flag ? fadePar:fadeMinPar);
		vis.selectAll(".par_rect_"+i).attr("opacity", flag ? 1:0.3);
		vis.selectAll(".par_label_"+i).attr("fill", flag ? "gray":"lightgray");
	};
	
	////////////////////////////////////////////////////////////////////////////////////// INIT
	var nLayers = thedata.spk_layers.length;
	var nParaverbal = thedata.par_layers.length;
	///////////////////////// MARGINS
	
	// step between bars
	var periodStep = thedata.period;
	var stepLegend = 14;
	var pixelStep = 10; 
	var leftMargin = 105;
	var rightMargin = 80;
	
	var topParvbMargin = stepLegend*nParaverbal+30; // space for paraverbal
	var graphTopMargin = 5; // inside graph only
	var graphBottomMargin = 20;
	var spaceForSpeakers = Math.max(100,stepLegend*nLayers+65);
	var totalW = 720;
	var totalH = topParvbMargin + spaceForSpeakers;
	var maxPeriods = thedata.maxPeriods;
	var graphW = totalW-rightMargin-leftMargin;

	// fetch values if edshow loaded with [i,o] intevall defined
	if(typeof(fromTextPart)=="undefined") {
		var initLInt=0;
		var initRInt=20;
		var maxTextPartsInt=maxPeriods;
	} else {
		var initLInt=fromTextPart
		var initRInt=toTextPart;
		var maxTextPartsInt=maxTextParts;
	}
		
	///////////////////////////////////////////////////////// DATA
	var nEnchantill = thedata.nPeriods;
	//console.log("nEnchantill:"+ nEnchantill);
	
	var scx = d3.scale.linear()
		.domain([0,maxTextPartsInt])
		.range([0,graphW]);
	var tx = function(d){return "translate("+scx(d)+",0)";};
	
	/////////////// DEFAULT ECHANTILLONNAGE
	var periodWantedInt = 3; // we take one i over "periodWantedInt"
	var periodWantedScaled = 3;
	var reEchantillonate = function(v) {
		echantillFactor = v;
		redraw();
	};   
	
	///////////////////////// PARAVERBAL SCALES
	// deprecated (same max for every prvbal)
	//var maxValueForParaverbal = d3.max( thedata.par_layers, function(d,i) { return d3.max(d); } );
	// now ONE max, and ONE scale PER paraverbal
	// todo: make it work !!! for the moment, cheating by declarating it above
	parYScales = new Array();
	for (i in thedata.par_layers) {
		var m = d3.max(thedata.par_layers[i]);
		var scaleParavb = d3.scale.linear()
        	.domain([0,m])
        	.range([topParvbMargin,graphTopMargin]);
        parYScales.push( scaleParavb );
        //console.log("found max value for paraverbal"+i+":"+m);
	}
	
	//////////////////////////////////////////////////////////////////
	var scaleEchantill = d3.scale.pow()
        .domain([0,100])
        .range([1,nEnchantill/2.0]);
	
	/////////////////////////////////////
	var vis = vizdiv.append("svg:svg")
		.attr("width", totalW)
		.attr("height", totalH);
	
	////////////////////////////////////////////////////////////////// SLIDER to update precision (jquery!!)
	var bottomDiv = vizdiv.append("div")
		.style("width",leftMargin-20)
		.style("position","absolute")
		.style("font-size",10)
		.style("left",5 )
		.style("top",totalH-50 );
	bottomDiv.append("span")
		.text("set precision to");
	bottomDiv.append("div")
		.style("display","inline-block")
		.style("width",leftMargin-20)
		.style("margin-top",5)
		.style("margin-bottom",5)
		.attr("id","slider_"+theId);
	bottomDiv.append("span")
		.attr("id","sliderlabel_"+theId)
		.text(parseInt(periodWantedScaled*periodStep)+" sentences");
	$("#slider_"+theId).slider({
		min:0,
		max:100,
		value:scaleEchantill.invert(periodWantedScaled),
		change: function(event, ui) {
			periodWantedScaled = scaleEchantill(ui.value);
			periodWantedInt = parseInt(periodWantedScaled);
			//console.log("changing echantill val:"+ui.value);
			//console.log("changing echantill scal:"+periodWantedScaled);
			d3.select("#sliderlabel_"+theId).text(parseInt(periodWantedScaled*periodStep)+" sentence");
			redraw();
		},
	});
	////////////////////////////////////////////////////////////////// CENTER TEXT and REFRESH button
	if(textPartsRefreshMode) {
		var mouse;
		vis.on("mousemove",function(){ mouse=d3.svg.mouse(this);computeMouseMove();})
			.on("mouseup",function(){ stopMouse();});
			
		var centerSelDiv = vizdiv.append("div")
			.style("text-align","center")
			.style("width",110)
			.style("position","absolute")
			.style("top",totalH-85);
		var centerText = centerSelDiv.append("div")
			.style("font-size",9)
			.style("margin",3)
			.text("...");
		var butRefresh = centerSelDiv.append("button")
			.attr("type","button")
			.style("height",10)
			.style("font-size",9)
			.attr("disabled","disabled")
			.text("refresh verbatim")
				.on("click",function() {sendSelectionRefresh();});
		var butPrev = centerSelDiv.append("button")
			.attr("type","button")
			.style("height",10)
			.style("font-size",9)
			.text("<<")
				.on("click",function() {sendSelectionPrevious();});
		var butNext = centerSelDiv.append("button")
			.attr("type","button")
			.style("height",10)
			.style("font-size",9)
			.text(">>")
				.on("click",function() {sendSelectionNext();});
		
		var selLeft=scx(initLInt);
		var selRight=scx(initRInt);
		var selLeftInt=initLInt;
		var selRightInt=initRInt;
		
		var decCenter = leftMargin - parseInt(centerSelDiv.style("width"))/2;
		var updateCenterSelection=function(){
			var selmid = decCenter + (selRight+selLeft)/2;
			centerSelDiv.style("left",selmid);
			centerText.text("["+selLeftInt+","+selRightInt+"]");
		};
		
		/////////////////////////////////////////////////////// BUTTON ACTIONS
		var sendSelectionPrevious=function(){
			if(selLeftInt!=0) {
				var intv = selRightInt-selLeftInt;
				var newLint = Math.max(selLeftInt-intv-1,0);
				var newRint = Math.max(selLeftInt-1,minSelWInt);
				setSelPositionInt(newLint,newRint);
				sendSelectionRefresh();$
			}
		};
		var sendSelectionNext=function(){
			if(selRightInt!=maxTextPartsInt) {
				var intv = selRightInt-selLeftInt;
				var newLint = Math.min(selRightInt+1,maxTextPartsInt-minSelWInt);
				var newRint = Math.min(selRightInt+intv+1,maxTextPartsInt);
				setSelPositionInt(newLint,newRint);
				sendSelectionRefresh();
			}
		};
		var sendSelectionRefresh=function(){
			updateCenterSelection();
			butRefresh.attr("disabled","disabled");
			console.log("setting refreshing interval to:["+selLeftInt+":"+selRightInt+"]");
			// then launch function in edShow to refresh textparts !
			getVerbatimParts(selLeftInt,selRightInt);
		};
		
		// initial position
		updateCenterSelection();
	}
	
	/////////////////////////////////////
	var visGraph = vis.append("svg:g")
		.attr("transform", "translate("+leftMargin+",0)")
		.attr("background-color","lightgray");
	var visScaleLegend = vis.append("svg:g")
		.attr("transform", "translate("+leftMargin+",0)");
		
	/////////////////////////////////////////////////////////////////////////////////// LEFT LEGEND (rects, text,..)
	vis.append("svg:rect")
		.attr("width", leftMargin)
		.attr("height",totalH)
		.attr("x",0)
		.attr("y",0)
		.attr("fill","white");
	vis.append("svg:line")
		.attr("x2",0)
		.attr("y2",topParvbMargin)
		.attr("x1",leftMargin-5)
		.attr("y1",topParvbMargin)
		.attr("stroke","gray");
	vis.append("svg:line")
		.attr("x2",leftMargin)
		.attr("y2",0)
		.attr("x1",leftMargin)
		.attr("y1",totalH)
		.attr("stroke","gray");
	vis.append("svg:line")
		.attr("x2",leftMargin)
		.attr("y2",topParvbMargin)
		.attr("x1",graphW+leftMargin)
		.attr("y1",topParvbMargin)
		.attr("stroke","gray");
	
	//////////////////////////////////////////////////////////////////////////////// MOUSE - SELECTION RECTANGLE(s)
	if(textPartsRefreshMode) {
		var drag=false,
			select=false,
			dragL=false,
			dragR=false;
		var clicX=0;
		var clicRectX=0;
		var minSelWInt=9;
		var minSelW=scx(minSelWInt);
		//////////////////////////
		var setSelPositionInt=function(li,ri) {
			selLeftInt=li;
			selRightInt=ri;
			setSelPosition(scx(selLeftInt),scx(selRightInt));
		}
		var setSelPosition=function(l,r) {
			// reshow "refresh verbatim" button
			butRefresh.attr("disabled",null);
			// constrain (only for mouseevents, cause previous/next are already done)
			selLeft=Math.max(0,l);
			if(!notDoing()) selLeft=Math.min(selRight-minSelW,selLeft);
			selRight=Math.min(graphW,r);
			if(!notDoing()) selRight=Math.max(selLeft+minSelW,selRight);
			// update all
			theSelRect.attr("x",selLeft).attr("width",selRight-selLeft);
			leftSelRect.attr("width",selLeft);
			rightSelRect.attr("x",selRight).attr("width",parseInt(graphW)-parseInt(selRight));
			leftSelG.attr("transform","translate("+selLeft+",0)");
			rightSelG.attr("transform","translate("+selRight+",0)");
		} 
		///////////////////////////////
		var dragSelBy=function(offs){
			var clicRectWidth=theSelRect.attr("width");
			var l = Math.max(0,parseInt(clicRectX)+parseInt(offs));
			var r = parseInt(l)+parseInt(clicRectWidth);
			setSelPosition(l,r);
		};
		var moveSelect=function(mx){
			d3.select("this").style("cursor","e-resize");
			if(mx>clicX)
				setSelPosition(clicX,mx);
			else
				setSelPosition(mx,clicX);
		};
		///////////////////////////////
		var computeMouseMove=function(){
			if(!notDoing()) {
				var mx = mouse[0]-leftMargin;
				//console.log("movingx:"+mx);
				if(drag) dragSelBy(mx-clicX);
				else if(select) moveSelect(mx);
				else if(dragL) {
					setSelPosition(mx,selRight);
				}
				else if(dragR) {
					setSelPosition(selLeft,mx);
				}
				selLeftInt=parseInt(scx.invert(selLeft));
				selRightInt=parseInt(scx.invert(selRight));
				// center text and button
				updateCenterSelection();
			}
		};
		///////////////////////////////
		var notDoing=function(){
			return (drag==false && select==false && dragL==false && dragR==false);
		}
		///////////////////////////////
		var startSelect=function(){
			if(notDoing()) {
				clicX=d3.svg.mouse(this)[0];
				select=true;
				//console.log("click:"+clicX);
			}
		};
		var startDrag=function(){
			if(notDoing()) {
				clicRectX=theSelRect.attr("x");
				clicX=d3.svg.mouse(this)[0];
				drag=true;
				//console.log("startdrag");
			}
		};
		var startDragLeft=function(){
			if(notDoing()) dragL=true;
		};
		var startDragRight=function(){
			if(notDoing()) dragR=true;
		};
		var stopMouse=function(){
			drag=select=dragL=dragR=false;
			//console.log("out");
		};
		//////////////////////////
		//vis.on("mousemove",computeMouseMove)		
		var selCanvas = vis.append("svg:g")
			.attr("id","selcanvas")
			.attr("transform","translate("+leftMargin+",0)");
		var theSelRect = selCanvas.append("svg:rect")
			.attr("x",selLeft)
			.attr("y",0)
			.attr("width",selRight-selLeft)
			.attr("height",totalH-graphBottomMargin)
			.attr("fill","white")
			.attr("opacity",0)
				.on("mousedown",startDrag)
				//.on("mousemove",computeMouseMove)
				.on("mouseup",stopMouse)
				.on("mouseover",function(d,i){d3.select(this).style("cursor","move");});
		var leftSelRect = selCanvas.append("svg:rect")
			.attr("x",0)
			.attr("y",0)
			.attr("width",selLeft)
			.attr("height",totalH)
			.attr("fill","gray")
			.attr("opacity",0.2)
				.on("mousedown",startSelect)
				//.on("mousemove",computeMouseMove)
				.on("mouseup",stopMouse);
		var rightSelRect = selCanvas.append("svg:rect")
			.attr("x",selRight)
			.attr("y",0)
			.attr("width",graphW-selRight)
			.attr("height",totalH)
			.attr("fill","gray")
			.attr("opacity",0.2)
				.on("mousedown",startSelect)
				//.on("mousemove",computeMouseMove)
				.on("mouseup",stopMouse);
		var leftSelG = selCanvas.append("svg:g")
			.attr("transform","translate("+selLeft+",0)");
		var rightSelG = selCanvas.append("svg:g")
			.attr("transform","translate("+selRight+",0)");
		var handW = 7;
		leftSelG.append("svg:rect")
			.attr("x",-handW)
			.attr("y",totalH-30)
			.attr("width",handW)
			.attr("height",30)
			.attr("stroke","gray")
			.attr("fill","white")
				.on("mousedown",startDragLeft)
				.on("mouseover",function(d,i){d3.select(this).style("cursor","w-resize");})
				//.on("mousemove",computeMouseMove)
				.on("mouseup",stopMouse);
		rightSelG.append("svg:rect")
			.attr("x",0)
			.attr("y",totalH-30)
			.attr("width",handW)
			.attr("height",30)
			.attr("stroke","gray")
			.attr("fill","white")
				.on("mousedown",startDragRight)
				.on("mouseover",function(d,i){d3.select(this).style("cursor","e-resize");})
				//.on("mousemove",computeMouseMove)
				.on("mouseup",stopMouse);
		leftSelG.append("svg:line")
			.attr("x1",0)
			.attr("x2",0)
			.attr("y1",0)
			.attr("y2",totalH-graphBottomMargin)
			.attr("stroke","gray")
			.attr("stroke-width",1)
				.on("mouseup",stopMouse);
		rightSelG.append("svg:line")
			.attr("x1",0)
			.attr("x2",0)
			.attr("y1",0)
			.attr("y2",totalH-graphBottomMargin)
			.attr("stroke","gray")
			.attr("stroke-width",1)
				.on("mouseup",stopMouse);
	}
	
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////// PARAVERBAL
	vis.selectAll("par_legendRects")
		.data(thedata.par_ids)
		.enter().append("svg:rect")
			.attr("class", function(d,i) { return "par_rect_"+i; })
			.attr("width", 10)
			.attr("height",10)
			.attr("x",5)
			.attr("y",function(d,i){return 6+i*stepLegend;})
			.attr("fill", function(d,i) { return thedata.par_colors[d[0]]; } )
			.on("click", function(d,i){ displayParvbBool[i]=!displayParvbBool[i]; })
			.on("mouseover", function(d,i){ showHideAllParaverbal(false); showHideParaverbal(i,true); })
			.on("mouseout", function(d,i){ showHideAllParaverbal(false); showHideAllParaverbal(true);});
	vis.selectAll("par_legendTexts")
		.data(thedata.par_ids)
		.enter().append("svg:text")
			.attr("class", function(d,i) { return "par_label_"+i; })
			.style("cursor","pointer")
			.attr("text-anchor", "left")
			.attr("x",20)
			.attr("y",function(d,i){return 6+i*stepLegend+10;})
			.attr("fill","gray")
			.text( function(d,i) {return d[1];} )
			.on("click", function(d,i){ displayParvbBool[i]=!displayParvbBool[i]; })
			.on("mouseover", function(d,i){ showHideAllParaverbal(false); showHideParaverbal(i,true); })
			.on("mouseout", function(d,i){ showHideAllParaverbal(false); showHideAllParaverbal(true); });	
			
	////////////////////////////////////////////////////////////////////////////////////////////////////////////// SPEAKER
	vis.selectAll("spk_legendRects")
		.data(thedata.spk_ids)
		.enter().append("svg:rect")
			.attr("class", function(d, i) { return "speakerColor_"+d[0]+" spk_rect spk_rect_"+i; })
			.attr("width", 10)
			.attr("height",10)
			.attr("x",5)
			.attr("y",function(d,i){return topParvbMargin + 6+i*stepLegend;})
			.on("mouseover", highlightSpk(false))
			.on("mouseout", highlightSpk(true));	
	vis.selectAll("spk_legendTexts")
		.data(thedata.spk_ids)
		.enter().append("svg:text")
			.attr("class", function(d, i) { return "spk_label spk_label_"+i; })
			.style("cursor","pointer")
			.attr("text-anchor", "left")
			.attr("x",20)
			.attr("y",function(d,i){return topParvbMargin + 6+i*stepLegend+10;})
			.attr("fill","gray")
			.text( function(d,i) {return d[1];} )
			.on("mouseover", highlightSpk(false))
			.on("mouseout", highlightSpk(true));	
	
	////////////////////////////////////////////////////////////////////////////////////////////////////////////// TEXT & LINES
	/////////// bottom right rect + label
/*
	vis.append("svg:rect")
		.attr("x",graphW+leftMargin)
		.attr("y",0)
		.attr("width", rightMargin)
		.attr("height",totalH)
		.attr("fill","white");
*/
	vis.append("svg:line")
		.attr("x2",graphW+leftMargin)
		.attr("y2",0)
		.attr("x1",graphW+leftMargin)
		.attr("y1",totalH)
		.attr("stroke","gray");
	vis.append("svg:text")
		.attr("x",leftMargin+graphW+5)
		.attr("y",totalH-5)
		.text("Sentences");

	var scale=1,
		decx=0;


	var scaleX = d3.scale.linear()
		.domain([0,nEnchantill])
		.range([0,graphW]);		
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// PARAVERBAL
	var par_Area = function(d,nPar) {
		var thearea = d3.svg.area()
			.x(function(d,i) { return decx + scaleX(i); })
			.y0(function(d) { return topParvbMargin; })
			.y1(function(d,i) { return parYScales[nPar](d); });
		return thearea(d);
	};
	
	var par_Layers = visGraph.selectAll("parpath")
		.data(thedata.par_layers)
		.enter().append("svg:path")
			.attr("class",function(d,i) {return "par_graph_"+i;} )
			.attr("display", function(d,i) { return displayParvbBool[i] ? "visible" : "none"; } )
			.attr("fill", function(d,i) { return thedata.par_colors[i]; })
			.attr("opacity",fadePar)
			.attr("stroke","gray")
			//.attr("opacity",0.3)
			.attr("d", function(d,i) {return par_Area(d,i);} );	
			//.attr("d", function(d,i) {return displayParvbBool[i] ? testArea(d,i) : " ";} );	
			
	///////////////////////////////////////////////////////////////////// SPEAKERS		
	var spk_StackData = d3.layout.stack().offset("zero")(thedata.spk_layers);
	var ymax = d3.max(spk_StackData, function(d) {
		return d3.max(d, function(d) { return d.y0 + d.y; });
	});
	var spk_Area = d3.svg.area()
		.x(function(d,i) { return decx + scaleX(i); })
		.y0(function(d) { return topParvbMargin + d.y0 * (totalH-topParvbMargin-graphBottomMargin)/ymax; })
		.y1(function(d) { return topParvbMargin + (d.y + d.y0) * (totalH-topParvbMargin-graphBottomMargin)/ymax; })
		.interpolate("linear");
	var spk_Layers = visGraph.selectAll("spkpath")
		.data(spk_StackData)
		.enter().append("svg:path")
			.attr("class", function(d,i) { return "speakerColor_"+thedata.spk_ids[i][0]+" spk_graph spk_graph_"+i; })
			.attr("title", function(d,i) {return thedata.spk_ids[i][1];}) // speaker name
			.attr("stroke","gray")
			.attr("d", spk_Area);					



	////////////////////////////////////////////////////////////////////////////// GRAPHS ARRAY MODIF (echantillonage)
	function mod_stack(dataIn,periodWantedInt) {
		var n = dataIn.length;
		return d3.range(n).map(function(lay) {
			var a = [], k;
			var laydatsource = dataIn[lay];
			cumul=0;
			for (k = 0; k < laydatsource.length; k++) {
				if(k!=0 && k%periodWantedInt==0) {
					a.push(cumul/parseFloat(periodWantedInt));
					cumul=0;
				}
				cumul+=laydatsource[k].y;
			}
			return a.map( function(d, i) {return {x: i, y: Math.max(0, d)}; });
		});
	};
	function mod_array(dataIn,periodWantedInt) {
		var n = dataIn.length;
		return d3.range(n).map(function(index) {
			var a = [], k;
			var thearray = dataIn[index];
			cumul=0;
			for (k = 1; k < thearray.length; k++) {
				cumul += thearray[k];
				//console.log("cumul:"+k)
				if(periodWantedInt==1 || (k!=0 && k%periodWantedInt==0)) {
					//console.log("add:"+k)
					a.push(cumul/periodWantedInt);
					cumul=0;
				}
			}
			return a;
		});
	};


	///////////////////////////////////////////////////////////////////////////////////////////////////////////
	function redraw() {
		// everything is based on nPeriodDisplayedWanted from slider (default = 40 periods in the window)
		//console.log("periodWantedInt:"+periodWantedInt);
		//console.log("REDRAWING with period:"+periodWantedInt);
		
		//////////////// UPDATE DATA & SCALES		
		spk_Data = mod_stack(thedata.spk_layers,periodWantedInt);
		par_Data = mod_array(thedata.par_layers,periodWantedInt);
		ttt=par_Data;
		
		scaleX.domain([0,par_Data[0].length-1]);
		scaleX.range([0,scale*graphW]);
		//console.log("maxI:"+par_Data[0].length);
		
		//////////////// UPDATE GRAPH PARAVERBAL
		var par_Area = function(d,nPar) {
			var thearea = d3.svg.area()
				.x(function(d,i) { return decx + scaleX(i); })
				.y0(function(d) { return topParvbMargin; })
				.y1(function(d,i) { return parYScales[nPar](d); });
			return thearea(d);
		};
		par_Layers.data(par_Data);
		par_Layers.attr("d", function(d,i) {return par_Area(d,i);} );
		//console.log("maxI:"+spk_Data[0].length);
		
		//////////////// UPDATE GRAPH SPEAKERS
		spk_StackData = d3.layout.stack().offset("zero")(spk_Data);
		ymax = d3.max(spk_StackData, function(d) {
			return d3.max(d, function(d) { return d.y0 + d.y; });
		});
		spk_Layers.data(spk_Data);
		spk_Area.x(function(d,i) { return decx + scaleX(i); })
				.y0(function(d) { return topParvbMargin + d.y0 * (totalH-topParvbMargin-graphBottomMargin)/ymax; })
				.y1(function(d) { return topParvbMargin + (d.y + d.y0) * (totalH-topParvbMargin-graphBottomMargin)/ymax; });
		spk_Layers.attr("d",spk_Area);
	}
	
	redraw();
	
	var fx = scx.tickFormat(10);
	///////// Generate x-ticks
	var gx = visScaleLegend.selectAll("g.x")
		.data(scx.ticks(10), String)
		.attr("transform", tx);
	gx.select("text")
		.text(fx);
	var gxe = gx.enter().insert("svg:g", "a")
		.attr("class", "x")
		.attr("transform", tx);
	gxe.append("svg:line")
		.attr("stroke","lightgray")
		.attr("y1", 0)
		.attr("y2", totalH-15);
	gxe.append("svg:text")
		.attr("y", totalH-15)
		.attr("dy", "1em")
		.attr("text-anchor", "middle")
		.text(fx);
	gx.exit().remove();

};
////////////////////////////////////////////////////