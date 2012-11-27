var oo = oo || {};

oo.filt = {};

// the basic stuff
oo.filt.filters = {};


oo.filt.events = {
	'change':'oo.filt.events.change',
	'clean':'oo.filt.events.clean',
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
	oo.log("[oo.filt.init]");
	oo.filt.on( oo.filt.events.add, oo.filt.add );
	oo.filt.on( oo.filt.events.remove, oo.filt.remove );
	oo.filt.on( oo.filt.events.reset, oo.filt.reset );
	oo.filt.on( oo.filt.events.clean, oo.filt.clean );
};

oo.filt.push = function(){
	oo.filt.trigger( oo.filt.events.change, oo.filt.filters );
}

oo.filt.add = function( eventType, data ){
	oo.log("[oo.filt.add] received", eventType, data);
	
	for (var f in data){
		oo.log( f, data[f]);
		if( typeof oo.filt.filters[f] == "object" ){
			// kind of merge
			oo.filt.filters[f].push( data[f] );
			$.unique( oo.filt.filters[f] );
		} else {
			oo.filt.filters[f] = data[f];
		}
	}
	oo.filt.push();
};

oo.filt.remove = function( eventType, data ){
	oo.log("[oo.filt.remove] received", eventType, data);
	for (var f in data){
		if( typeof oo.filt.filters[f] != "undefined" ){
			// which data?
		}
	}
		
	oo.filt.push();
};

/*
	example oo.filt.trigger( oo.filt.events.reset, {'type':[]} )
	This will delete the type field from the stored filters.
*/
oo.filt.reset = function( eventType, data ){
	for (var f in data){
		delete oo.filt.filters[f];
	};
	oo.filt.push();
};

oo.filt.clean = function( eventType, data ){
	oo.filt.filters = {};
	oo.filt.push();
};




