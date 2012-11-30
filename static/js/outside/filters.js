var oo = oo || {};

oo.filt = {};
oo.filt.filters = {};

oo.data = {}; // the json completed
oo.filt.data = {}; // data, filtered according to oo.filt.filters


oo.filt.events = {
	'change':'oo.filt.events.change',
	'clean':'oo.filt.events.clean',
	'add':'oo.filt.events.add',
	'replace':'oo.filt.events.replace',
	'remove':'oo.filt.events.remove',
	'reset':'oo.filt.events.reset'
};

oo.filt.cross = {
	'extent': function( item ){ return false; },
	'type': function( item ){ return true; }
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
	// ask for data
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.get_enquete_data,
		data: {}, 
		success:function(result){
			oo.log( "[oo.filt.init] get_enquete_data result:", result );
			oo.api.process( result, oo.filt.listen );
		}
	}));
	
}

oo.filt.listen = function( result ){
	oo.log("[oo.filt.listen]", result);
	oo.data = result;
	oo.filt.on( oo.filt.events.add, oo.filt.add );
	oo.filt.on( oo.filt.events.remove, oo.filt.remove );
	oo.filt.on( oo.filt.events.reset, oo.filt.reset );
	oo.filt.on( oo.filt.events.clean, oo.filt.clean );
};


oo.filt.execute = function(){
	oo.log("[oo.filt.execute]");

	oo.filt.data = {};

	for( var i in oo.data.objects ){
		oo.filt.data[ i ] = oo.data.objects[ i ];
	}

	// progressive filtering
	for( var type in oo.filt.filter ){
		for ( var i in oo.filt.data ){
			if ( ! oo.filt.cross[ type ]( o.data.objects[ i ] ) ){
				delete oo.filt.data[ i ]
			};
		}
	};

	oo.filt.trigger( oo.filt.events.change, oo.filt.filters );

}

/*
   Call the oo.filt.execute function which run through oo.data
   and filter according to oo.filt.filters.
   Selected items will be available inside oo.filt.data.
*/
oo.filt.push = function(){
	oo.log("[oo.filt.push]");
	clearTimeout( oo.filt.timer );
	oo.filt.timer = setTimeout( oo.filt.execute, 1000 );	
}

/*
	example oo.filt.trigger( oo.filt.events.add, {'place':['Paris','New York']} )
*/
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

/*
	example oo.filt.trigger( oo.filt.events.replace, {'type':replacement} )
*/
oo.filt.replace = function( eventType, data ){
	oo.log("[oo.filt.remove] received", eventType, data);
	for (var f in data){
		oo.filt.filters[f] = data[f];
	}
	oo.filt.push();
};

/*
	example oo.filt.trigger( oo.filt.events.remove, {'place':['Paris','New York']} )
*/
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

/*
	example oo.filt.trigger( oo.filt.events.clean, {} )
	This will delete the type field from the stored filters.
*/
oo.filt.clean = function( eventType, data ){
	oo.filt.filters = {};
	oo.filt.push();
};




