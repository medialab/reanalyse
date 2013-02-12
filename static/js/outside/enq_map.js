
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
	
	var objects = oo.enq.map.data;


	for (var i = 0; i < objects.features.length; i++) {
		// oo.log('i', objects.features[i])
		objects.features[i].counter = 0;
	};

	// oo.log('objects', objects)

	var nest = objects;

	for (var i in oo.filt.data){

		if ( oo.filt.data[i].location == null) continue;
		if ( oo.filt.data[i].filtered == false) continue;

		for ( j = 0; j <= nest.features.length; j++ ) {

			if ( typeof nest.features[j] == 'undefined' ) break;

			if ( nest.features[j].location == oo.filt.data[i].location ) {
				nest.features[j].counter++;
				break
			}

		};

	}

	// oo.log('nest', nest)

	var zoom = oo.enq.map.map.coordinate.zoom;

	for (var i = 0; i < nest.features.length; i++) {
		map.select('circle[data-location="' + nest.features[i].location + '"]')
			.transition()
				.duration(1500)
				.attr('r', (zoom + 1) * nest.features[i].counter / 10 );
	}
	
};





oo.enq.map.init = function ( objects ){

	oo.log('oo.enq.disabled.map', oo.enq.disabled.map)

	if ( typeof oo.enq.disabled.map == 'undefined' ) {
		d3.select('#map').style('display', 'block');
		d3.select('#timeline').style('margin-top', '0');
		return;	
	}

	oo.filt.on( oo.filt.events.change, oo.enq.map.update );

	// Map init

	oo.enq.map.map = mapbox.map('map');
    oo.enq.map.map.addLayer(mapbox.layer().id('fumoseaffabulazioni.map-80sq0fh2'));
	oo.enq.map.map.ui.zoomer.add();
	
	var nest = { type : "FeatureCollection", features : [] };

	for (var i in objects){

		var exist = false,
			j;

		if ( objects[i].location == null) continue;

		for ( j = 0; j <= nest.features.length; j++ ) {
			if ( typeof nest.features[j] == 'undefined' ) break;
			if ( nest.features[j].location == objects[i].location ) { exist = true; break; }
		};

		if ( exist == false ) {
			nest.features[j] = objects[i].coordinates;
			nest.features[j].counter = 0;
			nest.features[j].location = objects[i].location;
			nest.features[j].name = objects[i].coordinates.properties.name;
			// oo.log(i, objects[i].location, objects[i].coordinates.properties.name)
		}
		nest.features[j].counter++;
	}


	oo.enq.map.data = nest;

	// oo.log('objects', objects)
	oo.log('oo.enq.map.data', oo.enq.map.data)

    // return

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
        
      	first && svg.attr("width", f.map.dimensions.x)
	        	.attr("height", f.map.dimensions.y * 2)
				.style("margin-left", "0px")
				.style("margin-top", "0px")
			&& ( first = false );

      	circle.attr('r', function(d, i) { return (zoom + 1) * collection.features[i].counter / 10 })
      		.attr('cx', function(d, i) { return f.project(collection.features[i].geometry.coordinates)[0] })
            .attr('cy', function(d, i) { return f.project(collection.features[i].geometry.coordinates)[1] })
	      	.attr('lon', function(d, i) { return collection.features[i].geometry.coordinates[0]; })
	      	.attr('lat', function(d, i) { return collection.features[i].geometry.coordinates[1]; })
	      	.attr('data-location', function(d, i) { return collection.features[i].location; })
	      	.attr('title', function(d, i) { return collection.features[i].counter + ' in ' + collection.features[i].name; })
	      	.attr('rel', 'tooltip');
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

