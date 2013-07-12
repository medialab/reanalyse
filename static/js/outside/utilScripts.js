//////////////////////////////////////////////////////////////////// LAUNCH SEARCH
function initSearchForm(searchurl) {
	var form = $("#searchForm");
	form.submit(function(e) {
		if ($('#id_q').val()=="") {
			console.log("Search aborted (nothing was typed)");
			return false;
		}
		else {
			$("#id_searchsubmit").attr('disabled', true)
			launchSearch(searchurl,"");
			e.preventDefault(); 
		}
	});
}
function launchSearch(searchurl,extraParam) {
	var form = $("#searchForm");
	//console.log("Search launched");
	$('#ajaxContentSearchResults').html('<span class="vizLoadingSpinner"></span> Loading results ... &nbsp;')
	// GET parameters from the form, and from facets
	var paramlist = form.serialize();
	// facets ?
/*
	if(facetArray['texte'].length>0)
		paramlist += "&inTextes="+facetArray['texte'].toString();
	if(facetArray['speaker'].length>0)
		paramlist += "&inSpeakers="+facetArray['speaker'].toString();
*/
	// unsaved extra params (sort, paginate, ...)
	if(extraParam) paramlist += "&"+extraParam ;
	console.log("Search launched: "+searchurl+"?"+paramlist);
	
	//$.scrollTo($("#ajaxContentSearchResults"),500,{offset:-10});
	
	window.location.replace(searchurl+"?"+paramlist);
	
/*
	$.ajax({
		type: "GET",
		url: '{% url reanalyseapp.views.eSearch enquete.id %}?'+paramlist ,
		cache: false,
		success: function processAnswer(html) {
			//console.log('Search results received!');
			$('#ajaxContentSearchResults').html(html);
		}
	});
*/
	
	$("#id_searchsubmit").attr('disabled', false);

};

//////////////////////////////////////////////////////////////////// TO USE REGEXP in jquery selectors
// see http://james.padolsey.com/javascript/regex-selector-for-jquery/
jQuery.expr[':'].regex = function(elem, index, match) {
	var matchParams = match[3].split(','),
		validLabels = /^(data|css):/,
		attr = {
			method: matchParams[0].match(validLabels) ? 
						matchParams[0].split(':')[0] : 'attr',
			property: matchParams.shift().replace(validLabels,'')
		},
		regexFlags = 'ig',
		regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
	return regex.test(jQuery(elem)[attr.method](attr.property));
}



//////////////////////////////////////////////////////////////////// EVERYWHERE !!!!!!!!
function recalculateLeftMenuSize() {
	// done on loading, and if something (?) move in the page
	//var contentHeight = $("#content").height();
	//var leftMenuHeight = $("#leftmenucontent").height();
	// NB: 600px is the minimum height of the content div
	//$("#leftmenucontent").height(Math.max(600,leftMenuHeight,contentHeight)) ;
	//$("#leftmenucontent").height("100%") ;
}

//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
// fullscreen mode toggle
var fullscreenMode = false;
function toggleFullScreenMode() {
	if(!fullscreenMode) {
		$("#menu-fullscreen").addClass("selected");
		$("#sidebar-outer").toggle();
		$("#page-outer").removeClass("grid_9");
		$("#page-outer").addClass("grid_12");
		$("#page-outer").addClass("fullscreen");
	} else {
		$("#menu-fullscreen").removeClass("selected");
		$("#sidebar-outer").toggle();
		$("#page-outer").removeClass("fullscreen");
		$("#page-outer").removeClass("grid_12");
		$("#page-outer").addClass("grid_9");
	}
	fullscreenMode=!fullscreenMode;
	/*
	if(!fullscreenMode) {
		$("#sidebar-outer").toggle(dur);
		$("#page-outer").removeClass("grid_9");
		$("#page-outer").addClass("grid_12");
		$("#page-outer").addClass("fullscreen");
	}
	else {
		$("#sidebar-outer").toggle(dur);
		$("#page-outer").removeClass("fullscreen");
		$("#page-outer").removeClass("grid_12");
		$("#page-outer").addClass("grid_9");
	}
	fullscreenMode=!fullscreenMode;

	$(".setFullscreen.Off").toggle();
	$(".setFullscreen.On").toggle();
	*/
}

//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
// play with words display in Document view -  using css class
function resetVerbDisplayFilters() {
	$('#verb_css').remove();
	$('#verb_checkfilt_negative').removeAttr('checked');
	$('#ddcl-verb_selectfilt_pos-ddw input').removeAttr('checked'); // note ddcl cause we are using dropdownchecklist
}
function changeVerbatimWordsDisplay(wordsStr,css_prefix,showOnly) {
	var warray = wordsStr.split(/[\s,]+/); // split spaces + , + returns
	var css_str='<style id="verb_css">';
	
	var color_all = "#606060";
	var size_all = "12px";
	var color_select = "#DBDBDB";
	var size_select = "9px";
	if(showOnly) {
		color_all = "#DBDBDB";
		size_all = "9px";
		color_select = "#606060";
		size_select = "12px";
	}
	
	css_str+='.text_speaker {color:'+color_all+';font-size:'+size_all+';}';
	var reset=true;
	for(i in warray){
		var w = warray[i];
		if (w.length>0) {
			css_str += '.'+css_prefix+w+' {color:'+color_select+';font-size:'+size_select+';}';
			reset=false;
		}
	};
	console.log("css_str:"+css_str);
	css_str+='</style>';
	$("#verb_css").remove();
	var css_styl = $(css_str);
	if(!reset) $('html > head').append(css_styl);
}

//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////// SPEAKER / DOCUMENTS BROWSE & SELECTION
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////
// viz involved tooltips
var closemodalvizdialog;
function overlaymodalclickclose() {
 	if (closemodalvizdialog) {
  		$('.vizmodal').dialog('close');
 	}
 	//set to one because click on dialog (focus) box sets to zero 
 	closemodalvizdialog = 1;
}
function initVizInvolvedModals(getvizhtmlurl) {
	$(".vizinvolved").click( function(event) {
		var vizId = this.id.split("_")[1];
		$(".vizmodal").remove();
		$(".ui-dialog").remove();
		$.ajax({
			url: getvizhtmlurl,
			data: {'vizid':vizId},
			success: function(dat){
				var mod=$('<div class="vizmodal">');
				mod.html(dat.html);
				mod.dialog({
					title: dat.description,
					width: 750,
					modal: true,
					resizable: false,
					position: ['center',100],
					open: function() {
				  		closemodalvizdialog = 1;
				  		$(document).bind('click', overlaymodalclickclose);
				 	},
				 	focus: function() {
				  		closemodalvizdialog = 0;
				 	},
				 	close: function() {
				  		$(document).unbind('click');
				 	},
				});
				//closemodalvizdialog = 0;
			},
		});	
		//event.stopPropagation();
		return false;
	});
}


//////////////////////////////////////////////////////////////////
// SPEAKER BROWSE TABLE TOOLTIPS for selection
// DEPRECATED ?
function initSpeakerTableHeaderTooltips() {
	//Select all anchor tag with rel set to tooltip
	$('a[rel=sSelectionTooltip]').mouseover(function(e) {
		// todo: on mouseover, kill all others opened tooltips
		// or: make sure tooltip close when out !!
/*
		if($('#theSelTooltip').length!=0) {
			$('#theSelTooltip').remove();
		}
*/
		if($('#theSelTooltip').length==0) {
			me=$(this);
			//Grab the title attribute's value and assign it to a variable
			var tipcontent = $(this).parent().children('div.hiddentooltip').html();	
			//get the img because we need width and height
			var theIm = $(this).children('img');
			//Append the tooltip template and its value
			var theTip = $('<div id="theSelTooltip"><div class="tipBody">' + tipcontent + '</div></div>').appendTo($(this));
			var u=$(this).position();
			nx = u.left + theIm.width()/2 - theTip.width()/2;
			ny = u.top + theIm.height()/2 - theTip.height()/2;
			$('#theSelTooltip').css('position','relative');
			$('#theSelTooltip').css('float','left');
			$('#theSelTooltip').css('top', -10 );
			$('#theSelTooltip').css('left', 0 );
			
			$('#theSelTooltip').hover(
				function() { $.data(this, 'hover', true); },
				function() {
					$.data(this, 'hover', false);
					if(!this.parent().data('hover')) {
						this.parent().mouseout();
					}
				}
			).data('hover', true);
			
			$('#theSelTooltip a').click( function() {
				//console.log("selection made in tooltip - removing tooltip");
				$('#theSelTooltip').remove();
			});
		}
	})
	.mouseout(function() {
	 	if(!$('#theSelTooltip').data('hover')) {
			//Remove the appended tooltip template
			//console.log("removing tooltip");
			$('#theSelTooltip').remove();
			//$(this).children('div#theSelTooltip').remove();
		}
	});
}
//////////////////////////////////////////////////////////////////




//////////////////////////////////////////////////////////////////
// ON SPEAKER SET CLICK
function onSpeakerSetClick(eid,ssid) {
	// ajax ask for speaker list, then update local things
	$.ajax({
		type: "GET",
		url: '/reanalyse/e/'+eid+'/ss/'+ssid,
		cache: false,
		success: function receive(indata) { 
			deselectAllSpeakers();
			speakerIds = indata['speakersIds'] ;
			$("#speakerSetsList").children().removeClass("speakerSetSelected");
			$("#speakerSetsList").children('#spkset_'+ssid).addClass("speakerSetSelected");
			for (k in speakerIds) {
				var sid = speakerIds[k];
				//console.log("sset-selecting speaker:"+sid);
				var spkTr = $('#speakerTable tr#speaker_'+sid);
				selectSpeaker(spkTr[0]);
			};
		}
	});
};
//////////////////////////////////////////////////////////////////
// CREATE SETS (speakers table)
var comment=null;
function goCreateSpeakerSet(eid,theurl) {
	if ($('#inputSpkSetName').length==0) {
		$('html').click(function() {
			// if click outside, cancel
			//console.log("removing inputs!");
			newspksetdiv.remove();
		});
		var thelist = $('#speakerSetsList');
		var newspksetdiv = $('<li>').attr({'id':'goCreateSpeakerSetDiv'});
		var formSpkSet = $("<form>").attr({'class':'littleForm'});
		var inpute = $("<input>").attr({'type':'text','name':'name','id':'inputSpkSetName','class':'littleInputBox'})
		var butcancel = $("<a>").attr({'href':''}).text("cancel");
		var butok = $("<a>").attr({'href':''}).text("do it!");
		inpute.appendTo(formSpkSet);
		butcancel.appendTo(formSpkSet);
		butok.appendTo(formSpkSet);
		
		formSpkSet.appendTo(newspksetdiv);
		newspksetdiv.appendTo(thelist);
		
		butcancel.click( function() {
			newspksetdiv.remove();
		});
		inpute.click( function(event) {
			event.stopPropagation();
			event.preventDefault();
			return false;		
		});
		butok.click( function(event) {
			var newSetName = $('#inputSpkSetName').val();
			var nSpeaker = selectedSpeakerIds.length;
			speakers="";
			if(selectedSpeakerIds.length>0) {
				selectedSpeakerIds.forEach(function(e){
					speakers+=""+e+",";
				});
				// remove last ","
				speakers = speakers.slice(0,-1);
			}
			console.log("SPEAKERIDS:"+speakers);
			var data = formSpkSet.serialize();
			
			$.ajax({
				type: "GET",
				url: theurl,
				data: data+"&speakers="+speakers,
				cache: false,
				success: function receive(indata) {
					comment=indata;
					console.log("waouh");
					var ssId = indata['speakersetid'] ;
					console.log("speakerset created:"+ssId);
					formSpkSet.remove();
					$('#speakerSetsList').find("#nospeakerset").remove();
					var newElem = $("<li>").attr({'id':'spkset_'+ssId});
					var newLink = $("<a>").attr({'href':''});
					newLink.text("("+nSpeaker+") "+newSetName);
					newLink.appendTo(newElem);
					newLink.click( function(event) {
						onSpeakerSetClick(eid,ssId);
						return false;
					});
					$('#speakerSetsList').append(newElem);
					return false;
				}
			});
			
			event.stopPropagation();
			event.preventDefault();
			return false;
		});
	}
}
//////////////////////////////////////////////////////////////////
function goCreateTagCloud(eid,speakers) {
	if ($('#inputCloudCount').length==0) {
		// actually no button cancel (click outside cancel!)
		$('html').click(function() {
			// if click outside, cancel
			//console.log("removing inputs!");
			formCloudCount.remove();
		});		
		var div = $('#Cloud_SolrSpeakerTagCloud');
		var formCloudCount = $("<form>").attr({'class':'littleForm'});
		$("<span>").attr("class","goCreateVizForm").text(" with ").appendTo(formCloudCount);
		var inputte = $("<input>").attr({'type':'text','name':'noname','id':'inputCloudCount','class':'littleInputBox'});
		inputte.appendTo(formCloudCount);
		$("<span>").attr("class","goCreateVizForm").text("top words ").appendTo(formCloudCount);
		var butcancel = $("<a>").attr({'href':''}).text("cancel");
		var butok = $("<a>").attr({'href':''}).text("do-it!");
		//butcancel.appendTo(formCloudCount);
		butok.appendTo(formCloudCount);

		formCloudCount.appendTo(div);
		

		inputte.click( function(event) {
			event.stopPropagation();
			event.preventDefault();
			return false;		
		});
		butok.click( function() {
			param = {};
			param['count'] = $('#inputCloudCount').val();
			param['speakers'] = speakers;
			createVisualization(eid,'Cloud_SolrSpeakerTagCloud',param);
			formCloudCount.remove()
			return false;
		});
	}
}
//////////////////////////////////////////////////////////////////
// VISUALIZATION CREATION
function createVisualization(eid,vizType,moreparams) {
	//console.log("WILL BUILD VIZ");
	
	// check global vars
	if(moreparams['attributetypes']) var selectedAttributeTypesIds = moreparams['attributetypes'];
	else var selectedAttributeTypesIds = new Array();
	if(moreparams['speakers']) var selectedSpeakerIds = moreparams['speakers'];
	else var selectedSpeakerIds = new Array();
	if(moreparams['textes']) var selectedTexteIds = moreparams['textes'];
	else var selectedTexteIds = new Array();
		
	var dict={};
	dict['type']=vizType;
	var attributetypes="";
	var speakers="";
	var textes="";
	
	if (moreparams) {
		for (k in moreparams) {
			console.log("PARAMS:"+k+":"+moreparams[k]);
			dict[k] = moreparams[k];
		}
	} else console.log("PARAMS:empty");
	
	////////////////////////////////////////
	if(selectedAttributeTypesIds.length>0) {
		selectedAttributeTypesIds.forEach(function(e){
			attributetypes+=""+e+",";
		});
		// remove last ","
		attributetypes = attributetypes.slice(0,-1);
		dict['attributetypes']=attributetypes;
	}
	////////////////////////////////////////
	if(selectedSpeakerIds.length>0) {
		selectedSpeakerIds.forEach(function(e){
			speakers+=""+e+",";
		});
		// remove last ","
		speakers = speakers.slice(0,-1);
		dict['speakers']=speakers;
	}
	////////////////////////////////////////
	if(selectedTexteIds.length>0) {
		selectedTexteIds.forEach(function(e){
			textes+=""+e+",";
		});
		// remove last ","
		textes = textes.slice(0,-1);
		dict['textes']=textes;
	}
	////////////////////////////////////////
	
	// set spinner rolling
	$('.vizLoadingSpinner.'+vizType).attr('style','display:inline-block;');
	
	// Send AJAX to create visualization
	
	
	
	$.ajax({
		type: "GET",
		data: dict,
		dataType: "html",
		url: '/reanalyse/e/'+eid+'/v/make',
		cache: false,
		success: function updateProcessing(indata) {
			// remove spinner when done
			$('.vizLoadingSpinner.'+vizType).attr('style','display:none;');
			console.log("VIZU DONE");
			return false;
		}
	});
}


//////////////////////////////////////////////////////////////////
// BUILD AND CONNECT SCROLBAR FOR SPEAKER HAND-divs-MADE TABLE
function initSpeakerTableScrollBar() {
	// adjust inner width
	var realInnerWidth = $('#sContentWidthDiv').width();
	console.log('Width was adjusted from:'+$('.scrollHorizContent').width()+':to:'+realInnerWidth)
	$('.scrollHorizContent').width(realInnerWidth + 30);
	
	
	//scrollpane parts
	var scrollPane = $( ".sTableCenterHeader" ),
		scrollContent = $( ".scrollHorizContent" );
	
	//build slider
	var scrollbar = $( ".scroll-bar" ).slider({
		slide: function( event, ui ) {
			if ( scrollContent.width() > scrollPane.width() ) {
				scrollContent.css( "margin-left", Math.round(
					ui.value / 100 * ( scrollPane.width() - scrollContent.width() )
				) + "px" );
			} else {
				scrollContent.css( "margin-left", 0 );
			}
		}
	});
	
	//append icon to handle
	var handleHelper = scrollbar.find( ".ui-slider-handle" )
	.mousedown(function() {
		scrollbar.width( handleHelper.width() );
	})
	.mouseup(function() {
		scrollbar.width( "100%" );
	})
	.append( "<span class='ui-icon ui-icon-grip-dotted-vertical'></span>" )
	.wrap( "<div class='ui-handle-helper-parent'></div>" ).parent();
	
	//change overflow to hidden now that slider handles the scrolling
	scrollPane.css( "overflow", "hidden" );
	
	//size scrollbar and handle proportionally to scroll distance
	function sizeScrollbar() {
		var remainder = scrollContent.width() - scrollPane.width();
		var proportion = remainder / scrollContent.width();
		var handleSize = scrollPane.width() - ( proportion * scrollPane.width() );
		scrollbar.find( ".ui-slider-handle" ).css({
			width: handleSize,
			"margin-left": -handleSize / 2
		});
		handleHelper.width( "" ).width( scrollbar.width() - handleSize );
	}
	
	//reset slider value based on scroll content position
	function resetValue() {
		var remainder = scrollPane.width() - scrollContent.width();
		var leftVal = scrollContent.css( "margin-left" ) === "auto" ? 0 :
			parseInt( scrollContent.css( "margin-left" ) );
		var percentage = Math.round( leftVal / remainder * 100 );
		scrollbar.slider( "value", percentage );
	}
	
	//if the slider is 100% and window gets larger, reveal content
	function reflowContent() {
			var showing = scrollContent.width() + parseInt( scrollContent.css( "margin-left" ), 10 );
			var gap = scrollPane.width() - showing;
			if ( gap > 0 ) {
				scrollContent.css( "margin-left", parseInt( scrollContent.css( "margin-left" ), 10 ) + gap );
			}
	}
	
	//change handle position on window resize
	$( window ).resize(function() {
		resetValue();
		sizeScrollbar();
		reflowContent();
	});
	//init scrollbar size
	setTimeout( sizeScrollbar, 10 );//safari wants a timeout
}

//////////////////////////////////////////////////////////////////
// INIT VERBATIM TOOLTIPS
function initVerbatimTooltips() {
	$('a[rel=text_tooltip]').each(function() {
		$(this).qtip({
			content: $(this).attr("title"),
			show: 'mouseover',
			hide: 'mouseout',
			position: {
				corner: {
					target: 'bottomMiddle',
					tooltip: 'topMiddle'
				}
			},

			style: { 
				color:'black',
				name: 'blue',
				'font-weight':'bold',
				'font-family':'arial',
				
			}

		}).removeAttr('title');
	});
};




function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}




/* deprecated manual tooltip */
/*
function initVerbatimTooltipsOld() {
	//console.log("init verbatim tooltips");
	//Select all anchor tag with rel set to tooltip
	$('a[rel=text_tooltip]').mouseover(function(e) {
		if($('#theTextTooltip').length==0) {
			//Grab the title attribute's value and assign it to a variable
			var tip = $(this).attr('title');	
			 
			//Remove the title attribute's to avoid the native tooltip from the browser
			$(this).attr('title','');
			 
			//Append the tooltip template and its value
			//$(this).append('<div id="thetooltip"><div class="tipHeader"></div><div class="tipBody">' + tip + '</div><div class="tipFooter"></div></div>');	 
			$(this).append('<div id="theTextTooltip"><div class="tipBody">' + tip + '</div></div>');	 
			
			//Set the X and Y axis of the tooltip
			//var p=$(this).offset();
			var u = $(this).position();
			if($(this).hasClass('text_comment') || $(this).hasClass('text_break')) { 		//////// fixed position
				nx = 15;
				ny = 15;
			}
			else if ($(this).hasClass('text_time')) {	//////// fixed position, but on the left
				nx = 15 - $('#theTextTooltip').width();
				ny = 15;
			}
			else
			{
				ny = u.top + 12;
				nx = u.left + 17;
			}
			//var t=$(this).parent().position();
			//var z=$(this).parent().offset();
			
	//		console.log('offsx:'+p.left);
	//		console.log('positionx:'+u.left);
	//		console.log('positionparentx:'+t.left);
	//		console.log('offsetparentx:'+z.left);

			//console.log('nx:'+nx);
			//console.log('ny:'+ny);
			
			$('#theTextTooltip').css('top', ny );
			$('#theTextTooltip').css('left', nx );
			 
			//Show the tooltip with faceIn effect
			//$('#thetooltip').fadeIn('1000');
			//$('#thetooltip').fadeTo('10',0.8);
			
			// To keep tooltip displayed if over it
			var trigger = $(this);
			$(this).hover(
				function() { $.data(this, 'hover', true); },
				function() {
					$.data(this, 'hover', false);
				}
			).data('hover', true);
			
			$('#theTextTooltip').hover(
				function() { $.data(this, 'hover', true); },
				function() {
					$.data(this, 'hover', false);
					if(!this.parent().data('hover')) {
						this.parent().mouseout();
					}
				}
			).data('hover', false);
		}
	})
	.mousemove(function(e) {
	 
		//Keep changing the X and Y axis for the tooltip, thus, the tooltip move along with the mouse
		//$('#tooltip').css('top', e.pageY + 10 );
		//$('#tooltip').css('left', e.pageX + 20 );
		 
	}).mouseout(function() {
	 	if(!$('#theTextTooltip').data('hover')) {
			//Put back the title attribute's value
			$(this).attr('title',$('.tipBody').html());
			//Remove the appended tooltip template
			$(this).children('div#theTextTooltip').remove();
		}
	});
}
*/
//////////////////////////////////////////////////////////////////






//////////////////////////////////////////////////////////////////
// EXPAND TEXT EXTRACT IN SEARCH RESULTS
function toggleSentenceExtract(theAskingUrl,sentenceDomId,searchquery) {
	console.log('Toggle Sentence Extract of:'+sentenceDomId);
	var domTxt = $("#"+sentenceDomId+" .res_excerpt_txt");
	var domHtml = $("#"+sentenceDomId+" .res_excerpt_html");
	
	if(domTxt.css("display")=='block') {
		if(domHtml.html()=='') {
			domHtml.html('<span class="vizLoadingSpinner"></span> Loading...');
			$.ajax({
				type: "GET",
				url: theAskingUrl,
				data: {'highlight':searchquery},
				cache: false,
				success: function processAnswer(html) {
					console.log('Expanded extract received');
					domHtml.html(html);
					initVerbatimTooltips();
				}
			});
		}
		domTxt.css("display","none");
		domHtml.css("display","block");
	} else {
		domTxt.css("display","block");
		domHtml.css("display","none");	
	}
}
//////////////////////////////////////////////////////////////////






//////////////////////////////////////////////////////////////////
// BUILD TAG CLOUD FROM JSON
function initTagCloudsDeprecated(data) {
	console.log("dataMin:"+data.min);
	console.log("dataMax:"+data.max);
	
	$("#tagCloud").children().remove();
	$("<ul>").attr("id", "tagList").appendTo("#tagCloud");
	
	//create tags
	var minCount=data.min;
	var rangeCount=data.max-minCount;
	var minEm=0.7;
	var rangeEm=1;
	$.each(data.words, function(i, val) {
		//create item
		var li = $("<li>");
		//create link
		$("<a>").text(val.word).attr({rel:"tooltip",title:val.tip, href:"notyet"}).appendTo(li);
		
		//li.children().css("fontSize", (val.freq / 10 < 1) ? val.freq / 10 + 1 + "em": (val.freq / 10 > 2) ? "2em" : val.freq / 10 + "em");
		//scale tag size in [0.5,2]
		var freq = minEm + (val.count - minCount)*rangeEm/rangeCount;
		//console.log(freq);
		li.children().css("fontSize",  freq + "em");
		li.children().css("background-color",  val.color);
		//add to list
		li.appendTo("#tagList");
	});
	
	// update tooltips to build word tooltips
	initTooltips();
	
	if(data.words.length==0)
		var li = $("<li>");
		$("<a>").text("No words for that configuration").appendTo(li);
		li.appendTo("#tagList");
}
//////////////////////////////////////////////////////////////////
// MANAGE LEFT-MARGIN (SPEAKER NAMES)
function initSpeakersDivSizes(speakerIds) {	
	// Get width max of speaker_names
	wArray = $('.text_speaker_name').map(function() {
		return $(this).width();
	}).get();
	var maxW = Math.max.apply( Math, wArray );
	console.log("maxSpeakerNamesWidth:"+maxW);
	
	// Update leftmargin just to have space for speaker names
	$('.text_speaker').css("margin-left",maxW);

	// update position of each speaker name
	$('.text_speaker_name').each(function(index){
		$(this).css("left", 15 + maxW - $(this).width());
	});
}


//////////////////////////////////////////////////////////////////
// INIT TOOLTIPS
function initGeneralTooltips() {
	//Select all anchor tag with rel set to tooltip
	$('a[rel=generaltooltip]').mouseover(function(e) {
		if($('#theGeneralToolTip').length==0) {
			//Grab the title attribute's value and assign it to a variable
			var tip = $(this).attr('title');	
			 
			//Remove the title attribute's to avoid the native tooltip from the browser
			$(this).attr('title','');
			 
			//Append the tooltip template and its value
			//$(this).append('<div id="thetooltip"><div class="tipHeader"></div><div class="tipBody">' + tip + '</div><div class="tipFooter"></div></div>');	 
			$(this).append('<div id="theGeneralToolTip"><div class="tipBody">' + tip + '</div></div>');	 
			
			//Set the X and Y axis of the tooltip
			//var p=$(this).offset();
			var u=$(this).position();
			//var t=$(this).parent().position();
			//var z=$(this).parent().offset();
			
	//		console.log('offsx:'+p.left);
	//		console.log('positionx:'+u.left);
	//		console.log('positionparentx:'+t.left);
	//		console.log('offsetparentx:'+z.left);
			ny = u.top + 20;
			nx = u.left + 25;
	//		console.log('nx:'+nx);
	//		console.log('ny:'+ny);
			
			$('#theGeneralToolTip').css('top', ny );
			$('#theGeneralToolTip').css('left', nx );
			 
			//Show the tooltip with faceIn effect
			//$('#thetooltip').fadeIn('1000');
			//$('#thetooltip').fadeTo('10',0.8);
			
			// To keep tooltip displayed if over it
			var trigger = $(this);
			$(this).hover(
				function() { $.data(this, 'hover', true); },
				function() {
					$.data(this, 'hover', false);
				}
			).data('hover', true);
			
			$('#theGeneralToolTip').hover(
				function() { $.data(this, 'hover', true); },
				function() {
					$.data(this, 'hover', false);
					if(!this.parent().data('hover')) {
						this.parent().mouseout();
					}
				}
			).data('hover', false);
		}

	})
	.mousemove(function(e) {
		//Keep changing the X and Y axis for the tooltip, thus, the tooltip move along with the mouse
		//$('#tooltip').css('top', e.pageY + 10 );
		//$('#tooltip').css('left', e.pageX + 20 );
		 
	}).mouseout(function() {
	 	if(!$('#theGeneralToolTip').data('hover')) {
			//Put back the title attribute's value
			$(this).attr('title',$('.tipBody').html());
			//Remove the appended tooltip template
			$(this).children('div#theGeneralToolTip').remove();
		}
	});
}
//////////////////////////////////////////////////////////////////





////////////////////////////////////////////////
function produceIntroMenu(htmlurl) {
	
	console.log("hello boy! "+htmlurl);
	//$('#thecontent').load(htmlurl);
	//$.get(htmlurl,htmldata);


//	$.ajax({
//		type: "GET",
//		url: htmlurl,
//		cache: false,
//		success: function processHtml(json) {
//			//$('#thecontent').html(json);
//			//pat = /<h1>/;
//			//parts = htmldata.split(pat);
//			//console.log("hello boy! "+parts.length);
//			var obj = jQuery.parseJSON(json);
//			
//			
//			for (i=0;i<parts.length;i++) {
//				$('#thecontent').append('<div id="'+i+'">'+parts[i]+'</div>')
//			}
//		}
//	});
}

////////////////////////////////////////////////
function doGetAtUrl(theurl,func) {
	$.ajax({
		type: "GET",
		dataType: "json",
		url: theurl,
		cache: false,
		success: func
	});
}

function sayHello(str) {
	$("#logdiv").html(str);
}

////////////////////////////////////////////////
// Updating Processing values
function updateProcessingByAjax(enqueteid) {
	$.ajax({
		type: "GET",
		dataType: "json",
		url: '/reanalyse/e/'+enqueteid+'/json/statenquete/',
		cache: false,
		success: function updateProcessing(indata) { 
			var pjs = Processing.getInstanceById('processingSketchCanvas');
			console.log("JSON received:"+indata["names"]);
			pjs.addDocuments(indata["ids"],indata["names"],indata["nwords"]);
		}
	});
}

////////////////////////////////////////////////
// eBrowse, getting list of tag-it values
//function updateTagItValues(theurl) {
//	$.ajax({
//		type: "GET",
//		dataType: "json",
//		//data: 'deleteobjects',
//		url: theurl,
//		cache: false,
//		success: function processAnswer(indata) { $("#logdiv").html(indata); } //console.log('objects deleted, answer:'+indata); }
//	});
//}


////////////////////////////////////////////////