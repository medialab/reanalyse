
// 
// 
// Map
// 
// 

oo.enq.map.update = function( event, filters ){

	oo.log("[oo.enq.map.update]");

	var map = d3.select('#map');

	var items = map.selectAll('circle').each(function() {
		var item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	items.attr('data-status', 'inactive'); // Reset
	
	for ( var i in oo.filt.data ) {
		oo.filt.data[ i ].filtered &&
			map.select('circle[data-id="' + oo.filt.data[ i ].id + '"]')
				.attr('data-status', 'active');
	} // Set active

	var zoom = oo.enq.map.map.coordinate.zoom,
		inactiveSize = (zoom + 1) * 3 * .2,
		activeSize = (zoom + 1) * 3;

	items.each(function() {

		var item = d3.select(this),
			oldStatus = item.attr('data-status-old'),
			newStatus = item.attr('data-status');

		if ( ( oldStatus == 'active' ) && ( newStatus == 'inactive' ) ) {
			item.transition()
				.duration(1000)
				.attr('r', inactiveSize);
		} else if ( ( oldStatus == 'inactive') && ( newStatus == 'active') ) {
			item.transition()
				.duration(1500)
				.ease('elastic', 7, .8)
				.attr('r', activeSize);
		} else if (item.attr('data-status') == 'inactive') {
			item.transition()
				.duration(1000)
				.attr('r', inactiveSize);
		} else {
			item.transition()
				.duration(1500)
				.attr('r', activeSize);
		}

	})
	
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

    var f = {}, feature, collection,
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

    	var zoom = oo.enq.map.map.coordinate.zoom;
        
        first && circle.attr('r', (zoom + 1) * 3)
        	.style('stroke-width', (zoom + .4) * 3);

      	first && svg.attr("width", f.map.dimensions.x)
        	.attr("height", f.map.dimensions.y * 2)
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
            .attr('data-id', function(d) { return d.id })

            .on("click", function(d, i) {
            	
            	var item = d3.select(this);
	        	
	        	f.map.center({
	        		'lat' : item.attr('lat'),
	        		'lon' : item.attr('lon')
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
