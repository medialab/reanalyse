// d3.js code sample re-masterized by Mathieu Jacomy
// to adapt to make a doc timeline...

function drawTrend(selector, trend){
	var m = [10, 0, 20, 0],								// Margins
		w = 460 - m[1] - m[3],							// Width
		h = 100 - m[0] - m[2],							// Height
		parse = d3.time.format("%Y-%m-%d").parse;		// Date format
		
	// Scales. Note the inverted domain for the y-scale: bigger is up!
	var x = d3.time.scale().range([0, w]),
		y = d3.scale.linear().range([h, 0]);

	// X-axis.
	var xAxis = d3.svg.axis()
		.scale(x)
		.tickFormat(function(date){
			if(d3.time.format("%m")(date) == "01"){
				return d3.time.format("%Y")(date);
			} else {
				return d3.time.format("%b")(date);
			}
		})
		//.ticks(d3.time.months, 2)
		.tickSize(-h);

	// An area generator, for the light fill.
	var area = d3.svg.area()
		.interpolate("monotone")
		.x(function(d) { return x(d.date); })
		.y0(h)
		.y1(function(d) { return y(d.value); });

	// A line generator, for the dark stroke.
	var line = d3.svg.line()
		.interpolate("monotone")
		.x(function(d) { return x(d.date); })
		.y(function(d) { return y(d.value); });
	
	
	// Parse dates and numbers. We assume values are sorted by date.
	// Also compute the maximum value, needed for the y-domain.
	trend.values.forEach(function(d) { d.date = parse(d.week); d.value = +d.value; });
	trend.maxValue = d3.max(trend.values, function(d) { return d.value; });
	
	// Compute the minimum and maximum date.
	x.domain([
		d3.min(trend.values, function(d) { return d.date; }),
		d3.max(trend.values, function(d) { return d.date; })
	]);
	
	// Add an SVG element for the trend, with the desired dimensions and margin.
	var svg = d3.select(selector).selectAll("svg")
		.data([trend])
    .enter().append("svg")
		.attr("width", w + m[1] + m[3])
		.attr("height", h + m[0] + m[2])
    .append("g")
		.attr("transform", "translate(" + m[3] + "," + m[0] + ")");
	
	// Add the area path elements.
	svg.append("path")
		.attr("class", "area")
		.attr("d", function(d) { y.domain([0, d.maxValue]); return area(d.values); });

	// Add the x-axis.
	svg.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + h + ")")
		.call(xAxis);
	
	// Add the line path elements. Note: the y-domain is set per element.
	svg.append("path")
		.attr("class", "line")
		.attr("d", function(d) { y.domain([0, d.maxValue]); return line(d.values); });
	
}