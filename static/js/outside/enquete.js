var oo = oo || {};

oo.enq = {};

// plugin filters
oo.filt.cross.extent = function( item, ExtentObject ){


	// if item is in ExtentObject
    //	return true
    return false;
}

oo.filt.cross.extent = function( item, ExtentObject ){
	

	// if item is in ExtentObject
    //	return true
    return false;
}



oo.enq.timeline = {};
oo.enq.timeline.init = function(){
	
};
oo.enq.timeline.update = function(){

};


// Map

oo.enq.geo = {};

oo.enq.geo.init = function(){
	
	oo.filt.on( oo.filt.events.change, function(e, filters){
		oo.log(e, filters, oo.filt.data );
	});
};

oo.enq.geo.update = function ( objects ){

	oo.enq.geo.data = { type: "FeatureCollection", features:[]};

	for( var i in objects ){
		oo.enq.geo.data.features.push( objects[i].coordinates );
	}

	// Viz

	oo.enq.geo.map = mapbox.map('map');
    oo.enq.geo.map.addLayer(mapbox.layer().id('fumoseaffabulazioni.map-80sq0fh2'));

    layer = oo.enq.geo.d3layer().data(oo.enq.geo.data);
	oo.enq.geo.map.addLayer(layer);
	oo.enq.geo.map.extent(layer.extent());

	oo.enq.geo.map.ui.zoomer.add();
	
	oo.enq.geo.map.addCallback('panned', function(map, panOffset) {
		oo.filt.trigger( oo.filt.events.replace, {'extent': map.extent()} );
	});

	oo.enq.geo.map.addCallback('zoomed', function(map, zoomOffset) {
		setTimeout( function() {
    		oo.filt.trigger( oo.filt.events.replace, {'extent': map.extent()} );
    	}, 1000 );
	});

	oo.log('[oo.enq.geo]', oo.enq.geo)	

}

oo.enq.geo.d3layer = function() {

    var f = {}, bounds, feature, collection;

    var div = d3.select(document.body).append("div").attr('class', 'd3_layer'),
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

	oo.filt.on( oo.filt.events.init, function( event, data ){
		oo.log("[oo.enq.init]");

		oo.enq.geo.update( data.objects );
		oo.enq.timeline.update( data.objects );
	});


	return;

	d3.json( oo.api.urlfactory( oo.urls.get_enquete_data, 88 ), function(collection) {


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
			scaleY = d3.scale.linear().domain([minY, maxY]).range([0, 20]); // Set a proper height

		var timeline = d3.select('#timeline').append('svg'),
			brush = timeline.append('g'),
			circles = timeline.append('g')

		d3.selectAll('#timeline g').attr("transform", "translate(" + margin.right + "," + margin.top + ")");

		circles.selectAll(".dot")
			.data(data)
			.enter().append("circle")
			.attr('class', 'dot')
			.attr("cx", function(d) { return scaleX(d.x); })
			.attr("cy", function(d) { return scaleY(d.y); })
			.attr("data-time", function(d) { return d.x; })
			.attr("r", 4);

		// Behaviors

		

		$('#timeline').on('click', 'circle', function() {

			
			oo.log('range', range, 'width', width)

			// Missing right circle position

			var time = $(this).attr('data-time');

			var formattedTime = format.parse(time);

			var circleX = scaleX(formattedTime);

			oo.log('width/10', widthExtent, 'circleX', circleX)

			var left = circleX - widthExtent / 2;
			var right = circleX + widthExtent / 2;

			brushObj.extent([left, right]);
			brush.call(brushObj);

		});

		
		var brushObj = d3.svg.brush()
			.x(scaleX)
			.extent(scaleX.domain())
			.on("brushend", onBrush);

		brush.attr("class", "x brush")
			.call(brushObj)
			.selectAll("rect")
			.attr("y", - margin.top - 1 )
			.attr("height", $('#timeline').height() +1);

		var range = brushObj.extent();

		var widthExtent = ( range[1] - range[0] ) / 10;

		function onBrush() {

			// this returns a period of time

			var b = brushObj.empty() ? scaleX.domain() : brushObj.extent();
			oo.filt.trigger( oo.filt.events.replace, {'period': b } );
		}

		

	});
}


