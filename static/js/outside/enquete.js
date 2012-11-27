var oo = oo || {};

oo.enq = {};

oo.enq.d3layer = function() {
    
    var f = {}, bounds, feature, collection;

    var div = d3.select(document.body)
        .append("div")
        .attr('class', 'd3-vec'),
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
      feature.attr("d", path);
    };

    f.data = function(x) {
        collection = x;
        bounds = d3.geo.bounds(collection);
        feature = g.selectAll("path")
            .data(collection.features)
            .enter().append("path");
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

			// Geojson building

			var result = [];
			for (var i in collection.documents) {
				result.push(JSON.stringify(collection.documents[i].coordinates));
			}
			var jsonObj = '{"type": "FeatureCollection", "features": [' + result.toString() + ']}';
			collectionGeo = JSON.parse(jsonObj);

			// Map

			mapbox.auto('map', 'examples.map-vyofok3q', function(map) {
			    layer = oo.enq.d3layer().data(collectionGeo);
			    map.addLayer(layer);
			    map.extent(layer.extent());
			});

			// Timeline

			var format = d3.time.format("%Y-%m-%d");

				var data = d3.range(collection.documents.length).map(function(i) {
					return {
						x: format.parse(collection.documents[i].times[0].time),
						y: Math.floor(Math.random()*5)
					};
				});

				var width = $('#map').width();
				var height = $('#map').height();

				var min = d3.min(data, function (d) { return d.x });
				var max = d3.max(data, function (d) { return d.x });
				var x = d3.scale.linear().domain([min, max]).range([0, width]);
  				var y = d3.scale.linear().domain([0, 0]).range([0, 0]);

  				var timeline = d3.select('#timeline').append('svg').append("g");

  				timeline.attr("transform", "translate(0," + 30 + ")");

  				timeline.selectAll(".dot")
					.data(data)
			    	.enter().append("circle")
			    		.attr('class', 'dot')
			    		.attr("cx", function(d) { return x(d.x); })
			    		.attr("cy", function(d) { return d.y; })
						.attr("r", 3)
						.style('fill', 'white')
						.style('stroke', '#333')
						.style('stroke-width', '1.5px');
});
}


