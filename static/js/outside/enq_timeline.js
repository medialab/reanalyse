
// 
// 
// Timeline
// 
// 

var format = oo.filt.parser.datetime,
	size = {
			  width : $('#timeline').width(),
			 height : $('#timeline').height(),
		chartHeight : $('#timeline').height() * 9 / 11,
		brushHeight : $('#timeline').height() * 2 / 11
	},
	margin = { top: 30 };





oo.enq.timeline.update = function( event, filters ){

	oo.log("[oo.enq.timeline.update]");

	// Nest

	var nest = oo.nest( oo.filt.data, 
		function( d ){
			return format.parse(d.date).getFullYear()
		}, 
		function (a, b){
			return a.key < b.key ? -1 : a.key > b.key ? 1 : 0 }
	);

	// Set variables

	var steps = oo.enq.timeline.steps,
		rectWidth = oo.enq.timeline.rectWidth,
		minX = oo.enq.timeline.minX,
	    maxX = oo.enq.timeline.maxX,
	    rectTime = oo.enq.timeline.rectTime,
	    scaleX = oo.enq.timeline.scaleX,
		scaleY = oo.enq.timeline.scaleY;

	// Animate objects

	oo.enq.timeline.rectangles.dots
		.data(nest)
		.transition()
		.duration(1000)
		.attr('class', 'dot active')
		.attr("y", function(d) { return - scaleY(d.values.length) })
		.attr("height", function(d) { return scaleY(d.values.length) })
		.attr("data-id", function(d) { return d.id; });

	oo.enq.timeline.rectangles.lines
		.data(nest)
		.transition()
		.duration(1000)
		.attr("y", function(d) { return - scaleY(d.values.length) - 3; })

	oo.enq.timeline.rectangles.texts
		.data(nest)
		.text( function (d) { return d.values.length } )
		.transition()
		.duration(1000)
		.attr("y", function(d) { return - scaleY(d.values.length) - 5; });

};





oo.enq.timeline.init = function( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.timeline.update );

	// Nest

	var nest = oo.nest( objects, 
		function( d ){
			return format.parse(d.date).getFullYear()
		}, 
		function (a, b){
			return a.key < b.key ? -1 : a.key > b.key ? 1 : 0 }
	);

	// Set variables

	// oo.log('nest', nest)

	var steps = nest.length,
		rectWidth = d3.round( ( size.width - 100 ) / (steps) );

	oo.enq.timeline.minX = new Date(d3.min(objects, function (d) { return format.parse(d.date) }));
    oo.enq.timeline.maxX = new Date(d3.max(objects, function (d) { return format.parse(d.date) }));
	
	var rectTime = ( oo.enq.timeline.maxX - oo.enq.timeline.minX ) / ( steps - 1 );

	oo.enq.timeline.minY = 0;
	oo.enq.timeline.maxY = d3.max(nest, function (d) { return d.values.length });
	oo.enq.timeline.steps = steps;
	oo.enq.timeline.rectWidth = rectWidth;
	oo.enq.timeline.rectTime = rectTime;

	// Round scale edges

	oo.enq.timeline.minX.setDate(1);
	oo.enq.timeline.minX.setMonth(0);
	oo.enq.timeline.maxX.setDate(1);
	oo.enq.timeline.maxX.setMonth(12);

	// Set scales

	var scaleX = d3.time.scale()
			.domain([ oo.enq.timeline.minX, oo.enq.timeline.maxX ])
			.range([ 0, size.width - 100 ]),
		scaleY = d3.scale.linear()
			.domain([oo.enq.timeline.minY, oo.enq.timeline.maxY])
			.range([ 0, size.chartHeight - margin.top ]);

	oo.enq.timeline.scaleX = scaleX;
	oo.enq.timeline.scaleY = scaleY;

	// Containers

	oo.enq.timeline.svg        = d3.select('#timeline').append('svg').attr('width', 700);
	oo.enq.timeline.rectangles = oo.enq.timeline.svg.append('g').attr("transform", "translate(50, " + size.chartHeight + ")");
	oo.enq.timeline.axis       = oo.enq.timeline.svg.append('g').attr("transform", "translate(50, " + size.chartHeight + ")").attr('class', 'axis');
	oo.enq.timeline.brush      = oo.enq.timeline.svg.append('g').attr("transform", "translate(50, " + size.height + ")").attr("class", "brush");
	
	// Axis

	var axis = d3.svg.axis()
	    .scale(scaleX);

    oo.enq.timeline.axis.call(axis);

	// Chart

	var onClick = function(obj) {
		var domain = scaleX.domain(),
			circleTime = scaleX.invert( d3.select(obj).attr('x') ).getTime(),
			b = [circleTime, circleTime + rectTime],
			brushWidth = scaleX(b[1]) - scaleX(b[0]);
			
		d3.select("rect.extent")
			.transition()
			.duration(1000)
			.attr('x', scaleX(b[0]) )
			.attr('width', brushWidth ); // Width is fixed
		
		setTimeout( function() {
    		oo.enq.timeline.brush.call(brush.extent([b[0], b[1]]));
    		oo.filt.trigger( oo.filt.events.replace, { 'period': b } );
    	}, 1000 );
	}

	oo.enq.timeline.rectangles.backgrounds = oo.enq.timeline.rectangles.selectAll(".background")
		.data(nest)
		.enter().append('rect')
			.attr('class', 'background')
			.attr("x", function(d, i) { return i * rectWidth })
			.attr("y", function(d) { return - scaleY(d.values.length) })
			.attr("width", rectWidth)
			.attr("height", function(d) { return scaleY(d.values.length) })
			.attr("data-id", function(d) { return d.key; })
			.on("click", function() { onClick(this); })

	oo.enq.timeline.rectangles.dots = oo.enq.timeline.rectangles.selectAll(".dot")
		.data(nest)
		.enter().append('rect')
			.attr('class', 'dot active')
			.attr("x", function(d, i) { return i * rectWidth })
			.attr("y", function(d) { return - scaleY(d.values.length) })
			.attr("width", rectWidth)
			.attr("height", function(d) { return scaleY(d.values.length) })
			.attr("data-id", function(d) { return d.key })
			.on("click", function() { onClick(this); })

	oo.enq.timeline.rectangles.texts = oo.enq.timeline.rectangles.selectAll("text")
		.data(nest)
		.enter().append('text')
			.text( function (d) { return d.values.length } )
			.attr("x", function(d, i) { return i * rectWidth + 2; })
			.attr("y", function(d) { return - scaleY(d.values.length) - 5})
			.on("click", function() { onClick(this); });

	oo.enq.timeline.rectangles.lines = oo.enq.timeline.rectangles.selectAll(".line")
		.data(nest)
		.enter().append('rect')
			.attr('class', 'line')
			.attr("x", function(d, i) { return i * rectWidth })
			.attr("y", function(d) { return - scaleY(d.values.length) - 3})
			.attr("width", rectWidth)
			.attr("height", '1')
			.on("click", function() { onClick(this); });

	// Brush
	
	var brush = d3.svg.brush()
		.x(scaleX)
		// .extent(scaleX.domain()) // Used to set the initial 
		.on("brushend", brushEnd);

	oo.enq.timeline.brush.call(brush);

	oo.enq.timeline.brush.selectAll("rect")
		.attr("y", - size.brushHeight )
		.attr("height", size.brushHeight )

	oo.enq.timeline.brush.extent = d3.select('.brush > .extent');
	oo.enq.timeline.brush.background = d3.select('.brush > .background');

	// Activate filter
	
	function brushEnd() {
		var b = brush.empty() ? scaleX.domain() : brush.extent(); // this returns a period of time
		b = [ b[0].getTime(), b[1].getTime() ];
		oo.filt.trigger( oo.filt.events.replace, { 'period': b } );
	}

};

