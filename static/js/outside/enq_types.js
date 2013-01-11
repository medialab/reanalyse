
// 
// Types
// 
// 

oo.enq.types.update = function( event, filters ){

	// oo.log("[oo.enq.types.update]");

	// var items = d3.selectAll('#types li').each(function() {
	// 	var item = d3.select(this);
	// 	item.attr('data-status-old', item.attr('data-status'));
	// }); // Copy new status to old status

	// items.attr('data-status', 'inactive'); // Reset

	// var map = {};
	// for (var i in oo.filt.data) {
	// 	j = oo.filt.data[i].type;
	// 	if ( ( oo.filt.data[ i ].filtered.extent == 0 ) && ( oo.filt.data[ i ].filtered.period == 0 ) ) {
	// 		if(map.hasOwnProperty(j)) { 
	// 		    map[j]++;
	// 		} else {
	// 			map[j] = 1;
	// 		}
	// 	}
	// }

	// for( var i in map ){
	// 	d3.select('#types li[data-id="' + i + '"]')
	// 		.attr('data-status', 'active')
	// 		.html(map[i] + ' ' + i);
	// } // Set active

	// items.each(function() {

	// 	var item = d3.select(this);

	// 	if ( (item.attr('data-status-old') == 'active') && (item.attr('data-status') == 'inactive') ) {
	// 		item.transition()
	// 			.duration(1000)
	// 			.style('opacity', '0')
	// 			.style('height', '0px');
	// 	} else if ( (item.attr('data-status-old') == 'inactive') && (item.attr('data-status') == 'active') ) {
	// 		item.transition()
	// 			.duration(1000)
	// 			.style('opacity', '1')
	// 			.style('height', '30px');
	// 	}

	// })
	
};

oo.nest = function( objects, nester, sorter ){
	nested = {};
		// "key":{"key":"", "values":[ objects ... ]},
		// ...
	//]
	for (d in objects){
		var index = nester( objects[d] );
		if (typeof nested[ index ] == "undefined"){
			nested[ index ] ={ "key": index, "values":[] };
		}
		nested[ index ].values.push( objects[d] )
	}

	// refactoring array
	var remapped = []; for( var i in nested ){ remapped.push( nested[i] );}

	return remapped.sort(sorter);
	//	nested.sort( sorter )

}

oo.rollup = function( objects, nester, sorter ){
	nested = {};
	for (d in objects){
		var index = nester( objects[d] );
		if (typeof nested[ index ] == "undefined"){
			nested[ index ] ={ "key": index, "count":0 };
		}
		nested[ index ].count++;
	}
	var remapped = []; for( var i in nested ){ remapped.push( nested[i] );}
	return remapped.sort( sorter );
}

oo.enq.types.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.types.update );

	oo.log('objects', objects);


	var a = oo.nest( objects, 
		function( d ){ return d.type }, 
		function (a, b){ return a.values.length < b.values.length? 1: a.values.length > b.values.length? -1 : 0 }
	);
	oo.log( oo.rollup(objects, function( d ){ return d.type }, function( a, b){ return a.count < b.count? 1: a.count > b.count? -1 : 0 } ) )
	//oo.nest = d3.nest()
	//	.key(function (d) { return d.type })
		// .rollup(function(leaves) { return leaves.length; })
		// .sortKeys( function(a,b) { console.log( a, b); return 0 ; return a.values.length - b.values.length } )
		// .sortKeys(d3.ascending)
		// .sortValues( function(a,b) { console.log( a, b); return 0 ; return a.values.length - b.values.length } )
	//	.entries(objects);

	// nest.sortKeys(d3.ascending);

	oo.log('nest', a)

	// var map = {},
	// 	total = 0;

	// for (var i in objects) {
	// 	j = objects[i].type;
	// 	if(map.hasOwnProperty(j)) { 
	// 	    map[j]++;
	// 	} else {
	// 		map[j] = 1;
	// 	}
	// 	total++;
	// }


	// Density[] is the structure for timeline

	// for (var j = 0; j < map; j++) {

	// 	if ( j == 0 ) density = []; // Initialize array

	// 	if ( !density[j] ) {
	// 		density[j] = {};
	// 		density[j].name = i;
	// 		density[j].freq = map[i];
	// 		density[j].id = [];
	// 		// density[j].time = ( ticks[j] + ticks[j+1] ) * .5;
	// 	}
		
	// 	for (var i in objects) {
	// 		if ( ticks[j] <= collection[i].time && collection[i].time <= ticks[j+1] ) {
	// 			density[j].freq++;
	// 			density[j].id.push(collection[i].id);
	// 		}
	// 	}
	// }



	// oo.log(map)
	// oo.log('total', total)

	// var scaleX = d3.time.scale()
	// 	.domain([ 0, total ])
	// 	.range([ 0, size.width - 90 ]);

	// var types = d3.select('#types');

	// for (var i in map) {
	// 	types.append('div')
	// 	.attr('class', 'container')
	// 	.attr('data-id', i)
	// 	.attr('data-status', 'active')
	// 	.style('width', ( scaleX(map[i]) + 30 ) + 'px')
	// 	.html(map[i] + ' ' + i)
	// 	.append('div')
	// 	.attr('class', 'line')
	// 	.style('width', ( scaleX(map[i]) + 30 ) + 'px')
	// 	.style('height', '1px');
	// }

};


















