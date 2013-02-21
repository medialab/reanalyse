
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
	margin = { top: 30 };





oo.enq.timeline.update = function( event, filters ){

	oo.log("[oo.enq.timeline.update]");

	// Nest

	var nest = oo.nest( oo.filt.data, 
		function( d ){
			return format.parse(d.date).getFullYear()
		}, 
		function (a, b){ return a.date < b.date ? 1 : a.date > b.date ? -1 : 0 }
	);

	// Set variables

	var steps = nest.length,
		rectWidth = d3.round( ( size.width - 100 ) / (steps) ),
		minX = new Date(d3.min( oo.filt.data, function (d) { return format.parse(d.date) } )),
	    maxX = new Date(d3.max( oo.filt.data, function (d) { return format.parse(d.date) } )),
	    rectTime = ( maxX - minX ) / ( steps - 1);
		minY = 0,
		maxY = d3.max(nest, function (d) { return d.values.length });

	// Round scale edges

	minX.setDate(1);
	minX.setMonth(0);
	maxX.setDate(1);
	maxX.setMonth(12);

	// Set scales

	var scaleX = d3.time.scale()
			.domain([ minX, maxX ])
			.range([ 0, size.width - 100 ]),
		scaleY = d3.scale.linear()
			.domain([minY, maxY])
			.range([ 0, size.chartHeight - margin.top ]);

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
		function (a, b){ return a.date < b.date ? 1 : a.date > b.date ? -1 : 0 }
	);

	// Set variables

	var steps = nest.length,
		rectWidth = d3.round( ( size.width - 100 ) / (steps) ),
		minX = new Date(d3.min(objects, function (d) { return format.parse(d.date) })),
	    maxX = new Date(d3.max(objects, function (d) { return format.parse(d.date) })),
	    rectTime = ( maxX - minX ) / ( steps - 1);
		minY = 0,
		maxY = d3.max(nest, function (d) { return d.values.length });

	// Round scale edges

	minX.setDate(1);
	minX.setMonth(0);
	maxX.setDate(1);
	maxX.setMonth(12);

	// Set scales

	var scaleX = d3.time.scale()
			.domain([ minX, maxX ])
			.range([ 0, size.width - 100 ]),
		scaleY = d3.scale.linear()
			.domain([minY, maxY])
			.range([ 0, size.chartHeight - margin.top ]);

	// Containers

	var svg = d3.select('#timeline').append('svg');

	oo.enq.timeline.rectangles = svg.append('g').attr("transform", "translate(50, " + size.chartHeight + ")");
	oo.enq.timeline.axis       = svg.append('g').attr("transform", "translate(50, " + size.chartHeight + ")").attr('class', 'axis');
	oo.enq.timeline.brush      = svg.append('g').attr("transform", "translate(50, " + size.height + ")");
	
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
			
		oo.log('circleTime', circleTime)
		oo.log('rectWidth', rectWidth)
		oo.log('rectTime', rectTime)
		
		d3.select("rect.extent")
			.transition()
			.duration(1000)
			.attr('x', scaleX(b[0]) )
			.attr('width', brushWidth ); // Width is fixed
		
		setTimeout( function() {
    		oo.enq.timeline.brush.call(brushObj.extent([b[0], b[1]]));
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
	
	var brushObj = d3.svg.brush();

	oo.enq.timeline.brush.attr("class", "x brush")
		.call(brushObj.x(scaleX)
			.extent(scaleX.domain())
			.on("brushend", brushEnd))
		.selectAll("rect")
		.attr("y", - size.brushHeight )
		.attr("height", size.brushHeight );

	d3.select('rect.extent').attr("class", "extent transition");

	// Activate filter
	
	function brushEnd() {
		var b = brushObj.empty() ? scaleX.domain() : brushObj.extent(); // this returns a period of time
		b = [ b[0].getTime(), b[1].getTime() ];
		oo.filt.trigger( oo.filt.events.replace, { 'period': b } );
	}

};

