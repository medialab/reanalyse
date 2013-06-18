var oo = oo || {};

oo.enq = {};
oo.enq.map = {};
oo.enq.timeline = {};
oo.enq.types = {};
oo.enq.docs = {};
oo.enq.disabled = {};
oo.vars.map = {};


// 
// 
// Enquête
// 
// 

oo.enq.init = function(){
	oo.filt.on( oo.filt.events.init, function( event, data ){
		oo.log("[oo.enq.init]");
		oo.enq.map.init( data.objects );
		oo.enq.timeline.init( data.objects );
		oo.enq.types.init( data.objects );
		oo.enq.docs.init( data.objects );
	});
}

// 
// 
// Nest data
// 
// 

oo.nest = function( objects, nester, sorter ){

	nested = {};

	for (var d in objects){

		// Define object
		var index = nester( objects[d] ); // index

		// Check consistency of data
		if ( index == null || index.length == 0 ) continue;

		// Check group existence
		if ( typeof nested[ index ] == "undefined" ){ nested[ index ] = { "key": index, "values":[] }; }

		// Skip not filtered elements
		if ( typeof objects[d].filtered != 'undefined' && objects[d].filtered == false ) continue;

		// Push element
		nested[ index ].values.push( objects[d] );
	}

	// refactoring array
	var remapped = [];
	for ( var i in nested ) { remapped.push( nested[i] ); }

	// return remapped;
	return remapped.sort(sorter);

}


