
// 
// 
// Map
// 
//




oo.enq.map.update = function( event, filters ){

	oo.log("[oo.enq.map.update]");

	// Counter reset

	for (var i = 0; i < oo.enq.map.data.features.length; i++) {
		oo.enq.map.data.features[i].counter = 0;
	};

	// Nesting

	var nest = oo.enq.map.data;

	for ( var i in oo.filt.data ) {

		// oo.log(oo.filt.data[i].location)

		if ( oo.filt.data[i].location == null
			|| oo.filt.data[i].location.length == 0
			|| oo.filt.data[i].filtered == false ) continue; // Manage null location

		for ( var j = 0; j <= nest.features.length; j++ ) {

			if ( nest.features[j].location == oo.filt.data[i].location ) {
				nest.features[j].counter++;
				break
			}

		};

	}

	// Circles update

	circle
		.attr('data-original-title', function(d, i) {
			return 'Map <div class="white"></div>' + nest.features[i].counter + '/' + d3.select(this).attr('data-total')
				+ ' in ' + nest.features[i].name;
		})
		.transition()
			.duration(1000)
			.attr('r', function(d, i) {
				// oo.log('zoom', oo.enq.map.map.coordinate.zoom)
				// oo.log('norm', oo.vars.map.normalize(nest.features[i].counter) )
				// oo.log( (oo.enq.map.map.coordinate.zoom + 1) * .5 * oo.vars.map.normalize(nest.features[i].counter) )
				return (oo.enq.map.map.coordinate.zoom + 1) * .5 * oo.vars.map.normalize(nest.features[i].counter)
			});

};





oo.enq.map.init = function ( objects ){

	oo.log('oo.enq.disabled.map', oo.enq.disabled.map)

	// Case when map is disable

	if ( typeof oo.enq.disabled.map == 'undefined' ) {
		d3.select('#map').style('display', 'block');
		d3.select('#timeline').style('margin-top', '0');
		return;	
	}

	// Activate update

	oo.filt.on( oo.filt.events.change, oo.enq.map.update );

	// Map init

	oo.enq.map.map = mapbox.map('map');
    oo.enq.map.map.addLayer(mapbox.layer().id('fumoseaffabulazioni.map-80sq0fh2'));
	oo.enq.map.map.ui.zoomer.add();
	
	// Nesting

	var nest = { type : "FeatureCollection", features : [] };

	for (var i in objects){

		var j, exist = false;

		if ( objects[i].location == null || objects[i].location.length == 0 ) continue;

		for ( j = 0; j <= nest.features.length; j++ ) {
			if ( typeof nest.features[j] == 'undefined' ) break;
			if ( nest.features[j].location == objects[i].location ) { exist = true; break; }
		};

		if ( exist == false ) {
			nest.features[j] = objects[i].coordinates;
			nest.features[j].counter = 0;
			nest.features[j].location = objects[i].location;
			nest.features[j].name = objects[i].coordinates.properties.name;
		}

		nest.features[j].counter++;

	}

	oo.enq.map.data = nest;

	// Scale to represents circles

	oo.vars.map.normalize = d3.scale.linear()
		.domain([ 0, d3.max(oo.enq.map.data.features, function(d) { return d.counter; }) ])
		.range([ 0, 8 ]);

    // Layering

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
    	}, 500 );
	});
	
	//$('.zoomer.zoomin').trigger('click')

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

		if ( first ) {

			svg.attr("width", f.map.dimensions.x)
	        	.attr("height", f.map.dimensions.y * 2)
				.style("margin-left", "0px")
				.style("margin-top", "0px");

			circle
		      	.attr('lon', function(d, i) { return collection.features[i].geometry.coordinates[0]; })
		      	.attr('lat', function(d, i) { return collection.features[i].geometry.coordinates[1]; })
		      	.attr('data-total', function(d, i) { return collection.features[i].counter; })
		      	.attr('data-original-title', function(d, i) { return 'Map <div class="white"></div>' +
		      		collection.features[i].counter + '/' + collection.features[i].counter +
		      		' in ' + collection.features[i].name; })
		      	.attr('html', 'true')
	      		.attr('rel', 'tooltip')
	      		.attr('r', function(d, i) {
	      			return (oo.enq.map.map.coordinate.zoom + 1) * .5 * oo.vars.map.normalize(collection.features[i].counter)
				})
			
			first = false;
		}

      	circle
			.attr('cx', function(d, i) { return f.project(collection.features[i].geometry.coordinates)[0] })
	        .attr('cy', function(d, i) { return f.project(collection.features[i].geometry.coordinates)[1] })
	      	
    };

    f.data = function(data) {
        collection = data;
        bounds = d3.geo.bounds(collection);

        circle = g.selectAll("circle")
            .data(collection.features)
            .enter().append("circle")

            .on("click", function(d, i) {
            	
            	// It sets the map center and triggers the search

            	var item = d3.select(this);
	        	
	        	f.map.center({
	        		'lat' : item.attr('lat'),
	        		'lon' : item.attr('lon')
	        	}, true);

				setTimeout( function() {
	        		oo.filt.trigger( oo.filt.events.replace, {'extent': f.map.extent()} );
	        	}, 500 );

	        })

	        .on('mouseover', function(d, i) {
	        	
	        	// Set the position of tooltips

	        	var r = d3.select(this).attr('r');
	        	
	        	setTimeout( function() {
		        	
		        	var tt = d3.select('.tooltip'),
		        		top = tt.style('top'),
		        		left = tt.style('left');

		        	r = parseFloat(r);
		        	top = parseFloat(top.split('px')[0]) + r / 8 ;
		        	left = parseFloat(left.split('px')[0]) + r ;

		        	d3.select('.tooltip').style('top', top + 'px' );
		        	d3.select('.tooltip').style('left', left + 'px' );

		    	}, 0 );

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

