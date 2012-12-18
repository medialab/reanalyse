var oo = oo || {};

oo.enq = {};
oo.enq.map = {};
oo.enq.timeline = {};
oo.enq.types = {};
oo.enq.docs = {};

var circleSize = {
	'small' : 5,
	'medium' : 10,
	'big' : 50
};

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

	var items = d3.selectAll('#map circle').each(function() {
		var item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	items.attr('data-status', 'inactive'); // Reset
	
	for( var i in oo.filt.data ){
		d3.select('#map circle[data-id="' + oo.filt.data[i].id + '"]').attr('data-status', 'active');
	} // Set active

	items.each(function() {

		var item = d3.select(this);

		if ( (item.attr('data-status-old') == 'active') && (item.attr('data-status') == 'inactive') ) {
			item.transition()
				.duration(1000)
				.attr('r', circleSize.small);
		} else if ( (item.attr('data-status-old') == 'inactive') && (item.attr('data-status') == 'active') ) {
			item.transition()
				.duration(1500)
				.ease('elastic', 7, .8)
				.attr('r', circleSize.medium);
		} 
	})
	
};

for (var i=0, link; i<5; i++) {
	link = document.createElement("a");
	link.innerHTML = "Link " + i;
	link.onclick = function (num) {
		return function () {
			alert(num);
		};
	}(i);
document.body.appendChild(link);
}

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
        
        if (first) circle.attr('r', circleSize.medium);

      	first && svg.attr("width", f.map.dimensions.x)
          .attr("height", f.map.dimensions.y*2)
          .style("margin-left", "0px")
          .style("margin-top", "0px") && (first = false);

      	circle.attr('cx', function(d, i) { return f.project(collection.features[i].geometry.coordinates)[0] })
            .attr('cy', function(d, i) { return f.project(collection.features[i].geometry.coordinates)[1] })
	      	.attr('lon', function(d, i) { return collection.features[i].geometry.coordinates[0]; })
	      	.attr('lat', function(d, i) { return collection.features[i].geometry.coordinates[1]; });

    };

    f.data = function(x) {
        collection = x;
        bounds = d3.geo.bounds(collection);

        circle = g.selectAll("circle")
            .data(collection.features)
            .enter().append("circle")
            .attr('data-status', 'active')
            .attr('data-id', function(d) { return d.id });
        
        circle.on("click", function(d,i) {
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
	
	// d3.selectAll('#timeline .dot').attr('class', 'dot inactive');
	
	// for( var i in oo.filt.data ){
	// 	d3.select('#timeline .dot[data-id="' + oo.filt.data[i].id + '"]').attr('class', 'dot active');
	// }

	
};

oo.enq.timeline.init = function( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.timeline.update );

	var format = d3.time.format("%Y-%m-%d"),
		size = { width: $('#map').width() },
		margin = { top: $('#timeline').height() / 2 }
		steps = 10;

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

	scaleX = d3.time.scale()
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

	// Y Axes set up

	var minY = 0,
		maxY = d3.max(density, function (d) { return d.freq });

	scaleY = d3.scale.linear()
		.domain([minY, maxY])
		.range([ 0, 0 ]); // Set a proper height

	// Draw

	oo.enq.timeline.brush = d3.select('#timeline').append('svg').append('g')
		.attr("transform", "translate(" + 0 + "," + margin.top + ")");
	oo.enq.timeline.circles = d3.select('#timeline svg').append('g')
		.attr("transform", "translate(" + 0 + "," + margin.top + ")");

	oo.enq.timeline.circles.selectAll(".dot")
		.data(density)
		.enter().append("circle")
		.attr('class', 'dot active')
		.attr("cx", function(d) { return scaleX(d.time); })
		.attr("cy", 0)
		.attr("r", function(d) { return 2 + d.freq * 2 })
		.attr("data-id", function(d) { return d.id; });

	oo.enq.timeline.data = density;

	// Brush
	
	var brushObj = d3.svg.brush();

	oo.enq.timeline.brush.attr("class", "x brush")
		.call(brushObj.x(scaleX)
			.extent(scaleX.domain())
			.on("brushend", brushEnd))
		.selectAll("rect")
		.attr("y", - margin.top )
		.attr("height", $('#timeline').height());

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


// 
// Documents
// 
// 

oo.enq.docs.update = function( event, filters ){

	oo.log("[oo.enq.docs.update]");

	var items = d3.selectAll('#documents li').each(function() {
		var item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	items.attr('data-status', 'inactive'); // Reset
	
	for( var i in oo.filt.data ){
		d3.select('#documents li[data-id="' + oo.filt.data[i].id + '"]').attr('data-status', 'active');
	} // Set active

	items.each(function() {

		var item = d3.select(this);

		if ( (item.attr('data-status-old') == 'active') && (item.attr('data-status') == 'inactive') ) {
			item.transition()
				.duration(1000)
				.style('opacity', '0')
				.style('height', '0px');
		} else if ( (item.attr('data-status-old') == 'inactive') && (item.attr('data-status') == 'active') ) {
			item.transition()
				.duration(1000)
				.style('opacity', '1')
				.style('height', '19px');
		} 
	})
	
};

oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	var docs = d3.select('#documents');

	docs.selectAll("li")
		.data(objects)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.attr('data-status', 'active')
		.html(function(d) { return d.title; });

};


// 
// Types
// 
// 

oo.enq.types.update = function( event, filters ){

	oo.log("[oo.enq.types.update]");

	// d3.selectAll('#types li').attr('class', 'inactive'); // Reset
	
	// for( var i in oo.filt.data ){
	// 	d3.select('#types li[data-id="' + oo.filt.data[i].id + '"]').attr('class', 'active');
	// }

	d3.selectAll('#types li').remove();

	var map = {};
	for (var i in oo.filt.data) {
		j = oo.filt.data[i].type;
		if(map.hasOwnProperty(j)) { 
		    map[j]++;
		} else {
			map[j] = 1;
		}
	}

	var types = d3.selectAll('#types');

	for (var i in map) {
		types.append('li').html(map[i] + ' ' + i);
	}
	
};

oo.enq.types.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.types.update );

	var map = {};
	for (var i in objects) {
		j = objects[i].type;
		if(map.hasOwnProperty(j)) { 
		    map[j]++;
		} else {
			map[j] = 1;
		}
	}

	var types = d3.selectAll('#types');

	for (var i in map) {
		types.append('li').html(map[i] + ' ' + i);
	}

};



