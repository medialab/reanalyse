
// 
// 
// Timeline
// 
// 

var format = d3.time.format("%Y-%m-%d"),
	size = {
			  width : $('#map').width(),
			 height : $('#timeline').height(),
		chartHeight : $('#timeline').height() * 2 / 3,
		brushHeight : $('#timeline').height() * 1 / 3
	},
	margin = { top: 10 },
	steps = 7;



oo.enq.timeline.update = function( event, filters ){

	oo.log("[oo.enq.timeline.update]");

	// Collect useful fields

	for (i in oo.filt.data) {
		if ( !collection ) var collection = [];
		if ( ( oo.filt.data[ i ].filtered.extent == 0 ) ) {
			collection.push({
				time : format.parse(oo.filt.data[i].times[0].time).getTime(),
				id : oo.filt.data[i].id
			});
		}
	}

	// X Axes set up

	var   minX = d3.min(oo.data.objects, function (d) { return format.parse(d.times[0].time).getTime() }),
	      maxX = d3.max(oo.data.objects, function (d) { return format.parse(d.times[0].time).getTime() }),
		  unit = ( maxX - minX ) / steps,
		 ticks = [],
	   density = {};

	var scaleX = d3.time.scale()
		.domain([ minX, maxX ])
		.range([ 0, size.width ]);

	for (var i=0; i <= steps; i++) {
		ticks.push(minX + unit * i);
	};

	// Density[] is the structure for timeline

	for (var j = 0; j < steps; j++) {

		if ( j == 0 ) density = []; // Initialize array

		if ( !density[j] ) {
			density[j] = {};
			density[j].freq = 0;
			density[j].id = [];
			density[j].time = ( ticks[j] + ticks[j+1] ) * .5;
		}
		
		for (var i in collection) {
			if ( ticks[j] <= collection[i].time && collection[i].time <= ticks[j+1] ) {
				density[j].freq++;
				density[j].id.push(collection[i].id);
			}
		}
	}

	// Animate size of objects

	oo.enq.timeline.rectangles.selectAll(".dot")
		.data(density)
		.transition()
		.duration(1000)
		.attr('class', 'dot active')
		.attr("y", function(d) { return - scaleY(d.freq) })
		.attr("height", function(d) { return scaleY(d.freq) })
		.attr("data-id", function(d) { return d.id; });

};





oo.enq.timeline.init = function( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.timeline.update );

	// Collect useful fields

	var collection = d3.range(objects.length).map(function(i) {
		return {
		  time : format.parse(objects[i].times[0].time).getTime(),
			id : objects[i].id
		};
	});

	// X Axes set up

	var   minX = d3.min(collection, function (d) { return d.time }),
	      maxX = d3.max(collection, function (d) { return d.time }),
		  unit = ( maxX - minX ) / steps,
		 ticks = [],
	   density = {};

	var scaleX = d3.time.scale()
		.domain([ minX, maxX ])
		.range([ 0, size.width ]);

	for (var i=0; i <= steps; i++) {
		ticks.push(minX + unit * i);
	}; // Computation of ticks

	// Density[] is the structure for timeline

	for (var j = 0; j < steps; j++) {

		if ( j == 0 ) density = []; // Initialize array

		if ( !density[j] ) {
			density[j] = {};
			density[j].freq = 0;
			density[j].id = [];
			density[j].time = ( ticks[j] + ticks[j+1] ) * .5;
		}
		
		for (var i in collection) {
			if ( ticks[j] <= collection[i].time && collection[i].time <= ticks[j+1] ) {
				density[j].freq++;
				density[j].id.push(collection[i].id);
			}
		}
	}

	// Y Axes set up

	var minY = 0,
		maxY = d3.max(density, function (d) { return d.freq }),
		rectWidth = d3.round( size.width / steps );

	scaleY = d3.scale.linear()
		.domain([minY, maxY])
		.range([ 0, size.chartHeight ]); // Bar chart height

	// Draw shape

	var svg = d3.select('#timeline').append('svg');

	oo.enq.timeline.rectangles = svg.append('g').attr("transform", "translate(" + 0 + "," + size.chartHeight + ")");
	oo.enq.timeline.axis       = svg.append('g').attr("transform", "translate(" + 0 + "," + size.chartHeight + ")")
												.attr('class', 'axis');
	oo.enq.timeline.brush      = svg.append('g').attr("transform", "translate(" + 0 + "," + size.height + ")");
	
	// Axis

	
	oo.log('ticks', ticks)

	var ticksTimeFormat = [];
	var formatTick = d3.time.format("%m-%Y");

	for (var j = 0; j < ticks.length; j++) {
		oo.log('tick', ticks[j]);
		ticksTimeFormat.push(new Date(ticks[ j ]));
	}

	oo.log('ticksTimeFormat', ticksTimeFormat)

	var axis = d3.svg.axis()
	    .scale(scaleX)
	    .ticks(ticksTimeFormat.length)
	    .tickValues(ticksTimeFormat)
	    .tickFormat(d3.time.format("%m-%Y"));
	    // .tickFormat(d3.time.format('%Y'))
	    // .tickSubdivide(4);

    oo.enq.timeline.axis.call(axis)

	// Chart

	oo.enq.timeline.rectangles.selectAll(".dot")
		.data(density)
		.enter().append('rect')
		.attr('class', 'dot active')
		.attr("x", function(d) { return scaleX(d.time) - rectWidth * .5 ; })
		.attr("y", function(d) { return - scaleY(d.freq) })
		.attr("width", rectWidth)
		.attr("height", function(d) { return scaleY(d.freq) })
		.attr("data-id", function(d) { return d.id; });

	// Brush
	
	var brushObj = d3.svg.brush();

	oo.enq.timeline.brush.attr("class", "x brush")
		.call(brushObj.x(scaleX)
			.extent(scaleX.domain())
			.on("brushend", brushEnd))
		.selectAll("rect")
		.attr("y", - size.brushHeight )
		.attr("height", size.brushHeight);

	d3.select('rect.extent').attr("class", "extent transition");

	// Brush on Click

	$('#timeline').on('click', 'circle', function() {

		var domain = scaleX.domain(),
			circleTime = scaleX.invert( d3.select(this).attr('cx') ).getTime(),
			b = [circleTime - unit / 2, circleTime + unit / 2],
			brushWidth = scaleX(b[1]) - scaleX(b[0]);

		d3.select("rect.extent").transition()
			.duration(1000)
			.attr('x', scaleX(b[0]) )
			.attr('width', brushWidth ); // Width is fixed

		setTimeout( function() {
    		oo.enq.timeline.brush.call(brushObj.extent([b[0], b[1]]));
    		oo.filt.trigger( oo.filt.events.replace, { 'period': normBounds(b) } );
    	}, 1000 );

	});

	// Brush on Move

	function brushEnd() {

		var b = brushObj.empty() ? scaleX.domain() : brushObj.extent(); // this returns a period of time
		b = [ b[0].getTime(), b[1].getTime() ];
		oo.filt.trigger( oo.filt.events.replace, { 'period': normBounds(b) } );
	}

	// To round bounds limit according to ticks[]

	function normBounds( bounds ) {

		for ( var i = ticks.length; i >= 0; i-- ) {
			if ( bounds[0] + unit / 2 >= ticks[i] ) {
				bounds[0] = ticks[i] - 1;
				break;
			}
		}
		for ( var i = 0; i <= ticks.length; i++ ) {
			if ( bounds[1] - unit / 2 <= ticks[i] ) {
				bounds[1] = ticks[i] + 1;
				break;
			}
		}
		return bounds;
	};

};

