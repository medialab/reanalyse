/*
 * UIMTreeProcessor Class
 * version: 1.0 (11-16-2010)
 * 
 * Copyright (c) 2010 Vlad Shamgin (uimonster.com)
 * 
 * @requires jQuery v1.3.2 or later
 * @requires jsTree 1.0-rc1 or later
 *
 * Examples and documentation at: http://uimonster.com
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */

function UIMTreeProcessor(data, treeEl) {
	this.data = data;
	this.treeEl = treeEl;
}

UIMTreeProcessor.prototype.initTree = function(data){
	this.treeEl.jstree({
		"json_data" : {
			"data":data,
			"progressive_render":"true"
		},
		"plugins" : [ "themes", "default", "json_data" ],
		"themes" : {
			"theme" : "default",
			"dots" : false,
			"icons" : false
		},
		"core":{"animation":100},
		//"initially_open":["0"],
		"open_parents":false,
	});
	this.treeEl.jstree("close_all");
}

UIMTreeProcessor.prototype.doProcess = function(){
	//Find root:
	var _root = $(this.data).children(':first-child');
	var _a_feed = new Array();

	this.vsTraverse($(_root), _a_feed);

	var _treedata = [{"data":"<"+_root[0].nodeName+">","children":_a_feed, "state":"closed"}];
	this.initTree(_treedata);
}

UIMTreeProcessor.prototype.vsTraverse = function(node, arr){
	var _ch = $(node).children();
	
	for(var i=0; i<_ch.length; i++){
		var _vsArr = new Array();
		this.vsTraverse(_ch[i], _vsArr);
		//var _a_att = this.vsTraverseAtt(_ch[i]);
		var nodeAttsSt = this.vsTraverseAtt(_ch[i]);
/*
		if(null!=_a_att){
			_vsArr.push([{"data":"Attributes "+"["+_ch[i].nodeName+"]","children":_a_att, attr : { "class" : "uim_attr"}}]);
		}
*/
		if(null!=_ch[i].firstChild && 3==_ch[i].firstChild.nodeType){
			arr.push([{"data":"<"+_ch[i].nodeName+nodeAttsSt+"> " + _ch[i].firstChild.textContent,"children":_vsArr, "state":"closed"}]);
		}else{
			arr.push([{"data":"<"+_ch[i].nodeName+nodeAttsSt+"> ","children":_vsArr, "state":"open"}]);
		}
		
	}
}

UIMTreeProcessor.prototype.vsTraverseAtt = function(node){
	//var _a_atts = null;
	attsStr="";
	if(null!=node.attributes && node.attributes.length > 0){
		//_a_atts = new Array();
		for(var i=0; i<node.attributes.length; i++){
			attsStr+= " "+node.attributes[i].nodeName+'="'+node.attributes[i].nodeValue+'"';
			//_a_atts.push(node.attributes[i].nodeName + ":" + node.attributes[i].nodeValue);
		}
	}
	return attsStr;
	//return _a_atts;
}

