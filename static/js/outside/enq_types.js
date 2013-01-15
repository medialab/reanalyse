
// 
// Types
// 
// 

oo.enq.types.update = function( event, filters ){

	oo.log("[oo.enq.types.update]");

	var map = oo.nest( oo.filt.data, 
		function( d ){ return d.type }, 
		function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
	);

	// var count = oo.count(objects,
	// 	function( d ){ return d.type },
	// 	function( a, b){ return a.count < b.count? 1: a.count > b.count? -1 : 0 }
	// );

	oo.log('map', map)

	// return	

	var sum = d3.sum(map, function(d) { return d.values.length })
		num = map.length;

	// oo.log('num', num)

	var scaleX = d3.time.scale()
		.domain([ 0, sum ])
		.range([ 0, size.width ]);

	var types = d3.select('#types svg');

	var xPosition = 0;

	types.selectAll("rect.percentage")
		.each()
		// .transition()
		// .duration(1000)
		// .attr("width", function() {
		// 	oo.log(d3.select(this).attr('data-id'))
		// 	return 0;
		// });
	
};




oo.enq.types.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.types.update );

	var map = oo.nest( objects, 
		function( d ){ return d.type }, 
		function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
	);

	// var count = oo.count(objects,
	// 	function( d ){ return d.type },
	// 	function( a, b){ return a.count < b.count? 1: a.count > b.count? -1 : 0 }
	// );

	

	var sum = d3.sum(map, function(d) { return d.values.length });
		// num = map.length;

	// oo.log('num', num)

	var scaleX = d3.time.scale()
		.domain([ 0, sum ])
		.range([ 0, size.width ]);

	var types = d3.select('#types').append('svg');

	var xPosition = 0;

	for (var i in map) {
		
		var width = scaleX( map[i].values.length );
		
		var g = types.append('g')
			.attr('width', width)
			.attr('height', 30)
			.attr('transform', 'translate(' + xPosition + ', 0)');

		g.append('rect')
			.attr('class', 'background')
			.attr('width', width)
			.attr('height', 30)

		g.append('rect')
			.attr('class', 'percentage')
			.attr('data-id', map[i].key)
			.attr('width', width)
			.attr('height', 30)

		g.append('text')
			.attr('class', 'figure')
			.attr('width', width)
			.attr('height', 30)
			.attr('transform', 'translate(0,25)')
			.text('aaa')

		xPosition += width;
	}

};


















