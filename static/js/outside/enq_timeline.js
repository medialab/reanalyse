
// 
// 
// Timeline
// 
// 

var format = d3.time.format("%Y-%m-%d"),
	size = {
			  width : $('#timeline').width(),
			 height : $('#timeline').height(),
		chartHeight : $('#timeline').height() * 9 / 11,
		brushHeight : $('#timeline').height() * 2 / 11
	},
	margin = { top: 30 },
	steps = 7;



oo.enq.timeline.update = function( event, filters ){

	oo.log("[oo.enq.timeline.update]");

	
	// var map = oo.nest( objects, 
	// 		function( d ){ return format.parse(d.date).getTime() }, 
	// 		function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
	// 	)

	// oo.log('objects', objects)
	// oo.log('map', map)



	// Collect useful fields

	for (i in oo.filt.data) {
		if ( !collection ) var collection = [];
		if ( oo.filt.data[ i ].filtered == true ) {
			collection.push({
				time : format.parse(oo.filt.data[i].times[0].time).getTime(),
				id : oo.filt.data[i].id
			});
		}
	}

	// oo.log('collection', collection)

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

	// Animate objects

	oo.enq.timeline.rectangles.dots
		.data(density)
		.transition()
		.duration(1000)
		.attr('class', 'dot active')
		.attr("y", function(d) { return - scaleY(d.freq) })
		.attr("height", function(d) { return scaleY(d.freq) })
		.attr("data-id", function(d) { return d.id; });

	oo.enq.timeline.rectangles.lines
		.data(density)
		.transition()
		.duration(1000)
		.attr("y", function(d) { return - scaleY(d.freq) - 3; })
		.attr("data-id", function(d) { return d.id; });


	oo.enq.timeline.rectangles.texts
		.data(density)
		.text( function (d) { return d.freq } )
		.attr("data-id", function(d) { return d.id; })
		.transition()
		.duration(1000)
		.attr("y", function(d) { return - scaleY(d.freq) - 5; });

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
		.range([ 0, size.width - 100 ]);

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
		rectWidth = d3.round( ( size.width - 100 ) / steps );

	scaleY = d3.scale.linear()
		.domain([minY, maxY])
		.range([ 0, size.chartHeight - margin.top ]); // Bar chart height

	// Draw shape

	var svg = d3.select('#timeline').append('svg');

	// oo.enq.timeline.background = svg.append('g').attr("transform", "translate(0, " + size.chartHeight + ")");
	oo.enq.timeline.rectangles = svg.append('g').attr("transform", "translate(50, " + size.chartHeight + ")");
	oo.enq.timeline.axis       = svg.append('g').attr("transform", "translate(50, " + size.chartHeight + ")").attr('class', 'axis');
	oo.enq.timeline.brush      = svg.append('g').attr("transform", "translate(50, " + size.height + ")");
	
	// Axis

	for (var j = 0; j < ticks.length; j++) {
		if ( j == 0 ) var ticksTime = [];
		ticksTime.push(new Date(ticks[ j ]));
	} // Array of date ticks

	var axis = d3.svg.axis()
	    .scale(scaleX)
	    .ticks(ticksTime.length)
	    .tickValues(ticksTime)
	    .tickFormat(d3.time.format("%m-%Y"));

    oo.enq.timeline.axis.call(axis);

	// Chart

	var onClick = function(obj) {
		var domain = scaleX.domain(),
			circleTime = scaleX.invert( d3.select(obj).attr('x') ).getTime(),
			b = [circleTime, circleTime + unit],
			brushWidth = scaleX(b[1]) - scaleX(b[0]);
		d3.select("rect.extent")
			.transition()
			.duration(1000)
			.attr('x', scaleX(b[0]) )
			.attr('width', brushWidth ); // Width is fixed
		setTimeout( function() {
    		oo.enq.timeline.brush.call(brushObj.extent([b[0], b[1]]));
    		oo.filt.trigger( oo.filt.events.replace, { 'period': normBounds(b) } );
    	}, 1000 );
	}

	oo.enq.timeline.rectangles.backgrounds = oo.enq.timeline.rectangles.selectAll(".background")
		.data(density)
		.enter().append('rect')
		.attr('class', 'background')
		.attr("x", function(d) { return scaleX(d.time) - rectWidth * .5 ; })
		.attr("y", function(d) { return - scaleY(d.freq) })
		.attr("width", rectWidth)
		.attr("height", function(d) { return scaleY(d.freq) })
		.attr("data-id", function(d) { return d.id; })
		.on("click", function() { onClick(this); })

	oo.enq.timeline.rectangles.dots = oo.enq.timeline.rectangles.selectAll(".dot")
		.data(density)
		.enter().append('rect')
		.attr('class', 'dot active')
		.attr("x", function(d) { return scaleX(d.time) - rectWidth * .5 ; })
		.attr("y", function(d) { return - scaleY(d.freq) })
		.attr("width", rectWidth)
		.attr("height", function(d) { return scaleY(d.freq) })
		.attr("data-id", function(d) { return d.id; })
		.on("click", function() { onClick(this); })

	oo.enq.timeline.rectangles.texts = oo.enq.timeline.rectangles.selectAll("text")
		.data(density)
		.enter().append('text')
		.text( function (d) { return d.freq } )
		.attr("x", function(d) { return scaleX(d.time) - rectWidth * .5 + 2; })
		.attr("y", function(d) { return - scaleY(d.freq) - 5})
		.on("click", function() { onClick(this); });

	oo.enq.timeline.rectangles.lines = oo.enq.timeline.rectangles.selectAll(".line")
		.data(density)
		.enter().append('rect')
		.attr('class', 'line')
		.attr("x", function(d) { return scaleX(d.time) - rectWidth * .5 ; })
		.attr("y", function(d) { return - scaleY(d.freq) - 3})
		.attr("width", rectWidth)
		.attr("height", '1')
		.on("click", function() { onClick(this); });





	// Brush
	
	var brushObj = d3.svg.brush();

	oo.enq.timeline.brush.attr("class", "x brush")
		.call(brushObj.x(scaleX)
			.extent(scaleX.domain())
			.on("brushend", brushEnd))
		.selectAll("rect")
		.attr("y", - size.brushHeight )
		.attr("height", size.brushHeight );

	d3.select('rect.extent').attr("class", "extent transition");

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

