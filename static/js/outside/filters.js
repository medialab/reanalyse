var oo = oo || {};

oo.filt = {};

// the basic stuff
oo.filt.filters = {};


oo.filt.events = {
	'change':'oo.filt.events.change',
	'add':'oo.filt.events.add',
	'remove':'oo.filt.events.remove',
	'reset':'oo.filt.events.reset'
};

oo.filt.on = function( eventType, callback ){
	$(window).on( eventType, callback );
}

oo.filt.trigger = function ( eventType, data ){
	$(window).trigger( eventType, data );
}

/*
	Add listeners for add / remove / reset;
	format the response and trigger oo.filt.events.change.

*/
oo.filt.init = function(){
	
};

oo.filt.push = function(){
	oo.filt.trigger( oo.filt.events.change, oo.filt.filters );
}

oo.filt.add = function( eventType, data ){
	oo.filt.push();
};

oo.filt.remove = function( eventType, data ){
	oo.filt.push();
};

oo.filt.reset = function( eventType, data ){
	oo.filt.push();
};




