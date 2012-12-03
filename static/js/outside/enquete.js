var oo = oo || {};

oo.enq = {};

// plugin filters
oo.filt.cross.extent = function( item, ExtentObject ){
	// if item is in ExtentObject
    //	return true
    return false;
}

oo.enq.d3layer = function() {

	oo.log("[oo.enq.d3layer]")
    
    var f = {}, bounds, feature, collection;

    var div = d3.select(document.body)
        .append("div")
        .attr('class', 'd3_layer'),
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
      	.attr('lon', function(d, i) {
      		return collection.features[i].geometry.coordinates[0];
      	})
      	.attr('lat', function(d, i) {
      		return collection.features[i].geometry.coordinates[1];
      	});
    };

    f.data = function(x) {
        collection = x;
        bounds = d3.geo.bounds(collection);
        feature = g.selectAll("path")
            .data(collection.features)
            .enter().append("path")
            
            // On-click event

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
            new MM.Location(bounds[1][1], bounds[1][0]));
    };

    return f;
};



oo.enq.init = function(){

	oo.log("[oo.enq.init]")
	
	d3.json( oo.api.urlfactory( oo.urls.get_enquete_data, 88 ), function(collection) {

		//
		// Geojson building
		//

		var result = [];
		for (var i in collection.documents) {
			result.push(JSON.stringify(collection.documents[i].coordinates));
		}
		var jsonObj = '{"type": "FeatureCollection", "features": [' + result.toString() + ']}';
		collectionGeo = JSON.parse(jsonObj);


		//
		// Map
		//

	    var map = mapbox.map('map');
	    map.addLayer(mapbox.layer().id('fumoseaffabulazioni.map-80sq0fh2'));

	    layer = oo.enq.d3layer().data(collectionGeo);
		map.addLayer(layer);
		map.extent(layer.extent());

		map.ui.zoomer.add();
		//  Behaviors
		map.addCallback('panned', function(map, panOffset) {
			oo.filt.trigger( oo.filt.events.replace, {'extent': map.extent()} );
		});

		map.addCallback('zoomed', function(map, zoomOffset) {
			setTimeout( function() {
        		oo.filt.trigger( oo.filt.events.replace, {'extent': map.extent()} );
        	}, 1000 );
		});
		

		// Timeline

		var format = d3.time.format("%Y-%m-%d");

		var data = d3.range(collection.documents.length).map(function(i) {
			return {
				x: format.parse(collection.documents[i].times[0].time),
				y: Math.floor(Math.random()*5)
			};
		});

		var width = $('#map').width(),
			height = $('#map').height(),
			margin = {top: 20, right: 10};

		var minX = d3.min(data, function (d) { return d.x }),
			maxX = d3.max(data, function (d) { return d.x }),
			minY = d3.min(data, function (d) { return d.y }),
			maxY = d3.max(data, function (d) { return d.y }),
			scaleX = d3.scale.linear().domain([minX, maxX]).range([ 0, width - margin.right*2 ]),
			scaleY = d3.scale.linear().domain([minY, maxY]).range([0, 20]);

		var timeline = d3.select('#timeline').append('svg'),
			brush = timeline.append('g'),
			circles = timeline.append('g')

		// .attr("transform", "translate(" + margin.right + "," + margin.top + ")")

		circles.selectAll(".dot")
			.data(data)
			.enter().append("circle")
			.attr('class', 'dot')
			.attr("cx", function(d) { return scaleX(d.x); })
			.attr("cy", function(d) { return scaleY(d.y); })
			.attr("data-time", function(d) { return d.x; })
			.attr("r", 4);

		// Behaviors

		// $('#timeline').on('click', 'circle', function() {
		// 	var time = $(this).attr('data-time');
		// 	oo.filt.trigger( oo.filt.events.add, {'time':[time]} );
		// });

		
		var brushInit = d3.svg.brush()
			.x(scaleX)
			.on("brushend", onBrush);

		brush.attr("class", "x brush")
			.call(brushInit)
			.selectAll("rect")
			.attr("y", -1)
			.attr("height", $('#timeline').height() +1);

		function onBrush() {
			// this will return a date range to pass into the chart object 

			var b = brush.empty() ? scaleX.domain() : brush.extent();

			// oo.log('scaleX.domain())', scaleX.domain())
			// oo.log('brush.extent()', brush.extent())
 
		    // for(var i = 0; i < countriesCount; i++){
		    //     charts[i].showOnly(b);
		    // }
			    
		  // scaleX.domain(brush.extent());
		  // focus.select("path").attr("d", area);
		  // focus.select(".x.axis");
		}

		

	});
}


