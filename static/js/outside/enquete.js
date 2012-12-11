var oo = oo || {};

oo.enq = {};
oo.enq.map = {};
oo.enq.timeline = {};
oo.enq.types = {};
oo.enq.docs = {};

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
// Map
// 
// 

oo.enq.map.update = function( event, filters ){

	oo.log("[oo.enq.map.update]");

	d3.selectAll('#map path').attr('class', 'inactive'); // Reset
	
	for( var i in oo.filt.data ){
		d3.select('#map path[data-id="' + oo.filt.data[i].id + '"]').attr('class', 'active');
	}
	
};

oo.enq.map.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.map.update );

	// Map init

	oo.enq.map.map = mapbox.map('map');
    oo.enq.map.map.addLayer(mapbox.layer().id('fumoseaffabulazioni.map-80sq0fh2'));
	oo.enq.map.map.ui.zoomer.add();
	
	// Data

	oo.enq.map.data = { type : "FeatureCollection", features : [] };
	
	for( var i in objects ){
		oo.enq.map.data.features.push( objects[i].coordinates );
		oo.enq.map.data.features[i].id = objects[i].id;
	}

    layer = oo.enq.map.d3layer().data(oo.enq.map.data);
	oo.enq.map.map.addLayer(layer);
	oo.enq.map.map.extent(layer.extent());
	
	// Behaviors

	oo.enq.map.map.addCallback('panned', function(map, panOffset) {
		oo.filt.trigger( oo.filt.events.replace, {'extent': map.extent()} );
	});

	oo.enq.map.map.addCallback('zoomed', function(map, zoomOffset) {
		setTimeout( function() {
    		oo.filt.trigger( oo.filt.events.replace, {'extent': map.extent()} );
    	}, 1000 );
	});

}

oo.enq.map.d3layer = function() {

    var f = {}, bounds, feature, collection,
      div = d3.select(document.body).append("div").attr('class', 'd3_layer'),
      svg = div.append('svg'),
        g = svg.append("g");

    f.parent = div.node();

    f.project = function(x) {
      var point = f.map.locationPoint({ lat: x[1], lon: x[0] });
      return [point.x, point.y];
    };

    var first = true;
    f.draw = function() {
      first && svg.attr("width", f.map.dimensions.x)
          .attr("height", f.map.dimensions.y*2)
          .style("margin-left", "0px")
          .style("margin-top", "0px") && (first = false);

      path = d3.geo.path().projection(f.project);

      feature.attr("d", path)
      	.attr('lon', function(d, i) { return collection.features[i].geometry.coordinates[0]; })
      	.attr('lat', function(d, i) { return collection.features[i].geometry.coordinates[1]; });
    };

    f.data = function(x) {
        collection = x;
        bounds = d3.geo.bounds(collection);
        feature = g.selectAll("path")
            .data(collection.features)
            .enter().append("path")
            .attr('class', 'active')
            .attr('data-id', function(d) { return d.id })
            .on("click", function(d,i) {
            	f.map.center({
            		'lat' : d3.select(this).attr('lat'),
            		'lon' : d3.select(this).attr('lon')
            	}, true);
				setTimeout( function() {
	        		oo.filt.trigger( oo.filt.events.replace, {'extent': f.map.extent()} );
	        	}, 1000 );
            });
        return f;
    };

    f.extent = function() {
        return new MM.Extent(
            new MM.Location(bounds[0][1], bounds[0][0]),
            new MM.Location(bounds[1][1], bounds[1][0])
        );
    };

    return f;
};

// 
// 
// Timeline
// 
// 

oo.enq.timeline.update = function( event, filters ){

	oo.log("[oo.enq.timeline.update]");
	
	d3.selectAll('#timeline .dot').attr('class', 'dot inactive');
	
	for( var i in oo.filt.data ){
		d3.select('#timeline .dot[data-id="' + oo.filt.data[i].id + '"]').attr('class', 'dot active');
	}

	
};

oo.enq.timeline.init = function( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.timeline.update );

	var format = d3.time.format("%Y-%m-%d");

	oo.enq.timeline.data = d3.range(objects.length).map(function(i) {
		return {
			 x: format.parse(objects[i].times[0].time),
			 y: Math.floor(Math.random()*5),
			id: objects[i].id
		};
	});

	var width = $('#map').width(),
		height = $('#map').height(),
		margin = {top: 20, right: 20},
		minX = d3.min(oo.enq.timeline.data, function (d) { return d.x }),
		maxX = d3.max(oo.enq.timeline.data, function (d) { return d.x }),
		offset = ( maxX - minX ) / 15, // This circles' left/right margins
		minY = 0,
		maxY = d3.max(oo.enq.timeline.data, function (d) { return d.y }),
		scaleX = d3.time.scale().domain([minX.getTime() - offset, maxX.getTime() + offset]).range([ 0, width ]),
		scaleY = d3.scale.linear().domain([minY, maxY]).range([0, 20]); // Set a proper height

	oo.enq.timeline.brush = d3.select('#timeline').append('svg').append('g');
	oo.enq.timeline.circles = d3.select('#timeline svg').append('g');
	
	d3.selectAll('#timeline g').attr("transform", "translate(" + 0 + "," + margin.top + ")");

	oo.enq.timeline.circles.selectAll(".dot")
		.data(oo.enq.timeline.data)
		.enter().append("circle")
		.attr('class', 'dot active')
		.attr("cx", function(d) { return scaleX(d.x); })
		.attr("cy", function(d) { return scaleY(d.y); })
		.attr("data-id", function(d) { return d.id; })
		.attr("r", 4);

	// Brush behavior

	$('#timeline').on('click', 'circle', function() {

		var domain = scaleX.domain();
		var oneTenthDomain = ( domain[1] - domain[0] ) / 10;
		var circleTime = scaleX.invert( d3.select(this).attr('cx') ).getTime();
		var brushStart = circleTime - oneTenthDomain / 2;
		var brushEnd = circleTime + oneTenthDomain / 2;
		var brushWidth = scaleX(brushEnd) - scaleX(brushStart);

		d3.select("rect.extent").transition()
			.duration(1000)
			.attr('x', scaleX(brushStart) )
			.attr('width', brushWidth ); // Width is fixed

		setTimeout( function() {
    		oo.enq.timeline.brush.call(brushObj.extent([brushStart, brushEnd]));
    		oo.filt.trigger( oo.filt.events.replace, { 'period': [brushStart, brushEnd] } );
    	}, 1000 );

	});

	// Brush
	
	var brushObj = d3.svg.brush()

	oo.enq.timeline.brush.attr("class", "x brush")
		.call(brushObj.x(scaleX)
					  .extent(scaleX.domain())
					  .on("brushend", brushMove))
		.selectAll("rect")
		.attr("y", - margin.top - 1 )
		.attr("height", $('#timeline').height() +1);

	d3.select('rect.extent').attr("class", "extent transition");

	function brushMove() {
		var b = brushObj.empty() ? scaleX.domain() : brushObj.extent(); // this returns a period of time
		oo.filt.trigger( oo.filt.events.replace, {'period': b } );
	}

};


// 
// Documents
// 
// 

oo.enq.docs.update = function( event, filters ){

	oo.log("[oo.enq.docs.update]");

	d3.selectAll('#documents li').attr('class', 'inactive'); // Reset
	
	for( var i in oo.filt.data ){
		d3.select('#documents li[data-id="' + oo.filt.data[i].id + '"]').attr('class', 'active');
	}
	
};

oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	var docs = d3.select('#documents');

	docs.selectAll("li")
		.data(objects)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.html(function(d) { return d.title; });

};


// 
// Types
// 
// 

oo.enq.types.update = function( event, filters ){

	oo.log("[oo.enq.types.update]");

	d3.selectAll('#types li').attr('class', 'inactive'); // Reset
	
	for( var i in oo.filt.data ){
		d3.select('#types li[data-id="' + oo.filt.data[i].id + '"]').attr('class', 'active');
	}
	
};

oo.enq.types.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.types.update );

	// oo.log( objects )

	var types = d3.select('#types');

	types.selectAll("li")
		.data(objects)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.html(function(d) { return d.type; });

};



