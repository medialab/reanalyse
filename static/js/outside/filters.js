var oo = oo || {};

oo.filt = {};
oo.filt.filters = {};

oo.data = {}; // the json completed
oo.filt.data = {}; // data, filtered according to oo.filt.filters


// Events Types

oo.filt.events = {
	    'add':'oo.filt.events.add',
	 'change':'oo.filt.events.change',
	  'clean':'oo.filt.events.clean',
	   'init':'oo.filt.events.init',
	'replace':'oo.filt.events.replace',
	 'remove':'oo.filt.events.remove',
	  'reset':'oo.filt.events.reset'
};


oo.filt.parser = {
	datetime: d3.time.format("%Y-%m-%d")
}; // Parsers


// Filters plug-in

oo.filt.cross = oo.filt.cross || {
	'extent': function( item, filter ){
		var bounds = filter,
			 point = item.coordinates.geometry.coordinates;
		return point[1] < bounds.north && point[1] > bounds.south && point[0] < bounds.east && point[0] > bounds.west;
	},
	'period': function( item, filter ){
		var item_time = oo.filt.parser.datetime.parse( item.times[0].time ).getTime();
		return item_time > filter[0] && item_time < filter[1];
	},
	'type': function( item, filter ){
		return item.type == filter
	},
	'category': function( item, filter ){
		return item.categories[0].category == filter
	},
	'phase': function( item, filter ){
		return item.phases[0].phase == filter
	},
	'article': function( item, filter ){
		// if ( item.articles.length == 0 ) return false;
		return item.articles[0].article == filter
	}
};


/*
	On / Trigger
*/

oo.filt.on = function( eventType, callback ){
	$(window).on( eventType, callback );
};

oo.filt.trigger = function ( eventType, data ){
	$(window).trigger( eventType, data );
};


/*
	Load data
*/

oo.filt.init = function(){

	oo.log("[oo.filt.init]");
	
	$.ajax( $.extend( oo.api.settings.post,{
		url: oo.urls.get_enquete_data,
		data: {},
		success:function( result ){
			oo.log( "[oo.filt.init]", result );
			oo.api.process( result, oo.filt.listen );
		}
	}));
};


/*
	Add listeners for add / clean / remove / replace / reset;
*/

oo.filt.listen = function( result ){

	oo.log("[oo.filt.listen]");
	
	oo.data = result;
	oo.filt.trigger( oo.filt.events.init, oo.data );

	oo.filt.on( oo.filt.events.add, oo.filt.add );
	oo.filt.on( oo.filt.events.clean, oo.filt.clean );
	oo.filt.on( oo.filt.events.remove, oo.filt.remove );
	oo.filt.on( oo.filt.events.replace, oo.filt.replace );
	oo.filt.on( oo.filt.events.reset, oo.filt.reset );

};





/*
	Call the oo.filt.execute function after a predefined delay
*/

oo.filt.push = function(){
	
	// oo.log("[oo.filt.push]");

	clearTimeout( oo.filt.timer );
	oo.filt.timer = setTimeout( oo.filt.execute, 100 );	
};


/*
	Run through oo.data and filter according to oo.filt.filters.
	Selected items will be available inside oo.filt.data.
	Format the response and trigger oo.filt.events.change.
*/

oo.filt.execute = function(){

	oo.filt.data = {};

	// old modified progressive filtering (added filtered field - true for visible)

	for( var i in oo.data.objects ){
		oo.filt.data[ i ] = oo.data.objects[ i ];
		oo.filt.data[ i ].filtered = true;
	}; // copy original data

	for( var type in oo.filt.filters ){
		for ( var i in oo.filt.data ){
			if ( ! oo.filt.cross[ type ]( oo.data.objects[ i ], oo.filt.filters[type] ) ){
				// delete oo.filt.data[ i ]
				oo.filt.data[ i ].filtered = false;
			} else {
			}
		}
	};

	// oo.log("[oo.filt.execute]", oo.filt.filters, oo.filt.data);

	oo.filt.trigger( oo.filt.events.change, oo.filt.filters );

};







/*
	This will add a filter.
	ex. oo.filt.trigger( oo.filt.events.add, {'place':['Paris','New York']} )
*/

oo.filt.add = function( eventType, data ){

	oo.log("[oo.filt.add] received");
	
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
	This will empty filters.
	ex. oo.filt.trigger( oo.filt.events.clean, {} )
*/

oo.filt.clean = function( eventType, data ){

	oo.log("[oo.filt.clean]");

	oo.filt.filters = {};
	oo.filt.push();
};


/*
	This will remove filter item/s.
	ex. oo.filt.trigger( oo.filt.events.remove, {'place':['Paris','New York']} )
*/

// oo.filt.remove = function( eventType, data ){

// 	oo.log("[oo.filt.remove]");
	
// 	for (var f in data){
// 		if( typeof oo.filt.filters[f] != "undefined" ){
// 			// which data?
// 		}
// 	}
// 	oo.filt.push();
// };


/*
	This will replace the type field.
	ex. oo.filt.trigger( oo.filt.events.replace, {'type':replacement} )
*/

oo.filt.replace = function( eventType, data ){

	oo.log("[oo.filt.replace]");

	for (var i in data) oo.filt.type = i; // Set filter type

	for (var f in data) {
		oo.filt.filters[f] = data[f];
	};
	oo.filt.push();
};


/*
	This will delete the type field.
	ex. oo.filt.trigger( oo.filt.events.reset, {'type':[]} )
*/

oo.filt.reset = function( eventType, data ){

	oo.log("[oo.filt.reset]");

	for (var f in data) {
		delete oo.filt.filters[f];
	};
	oo.filt.push();
};






