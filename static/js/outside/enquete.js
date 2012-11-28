var oo = oo || {};

oo.enq = {};

oo.enq.d3layer = function() {

	oo.log("[oo.enq.d3layer]")
    
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

			var width = $('#map').width(),
				height = $('#map').height(),
				margin = {top: 20, right: 10};


			var minX = d3.min(data, function (d) { return d.x });
			var maxX = d3.max(data, function (d) { return d.x });
			var minY = d3.min(data, function (d) { return d.y });
			var maxY = d3.max(data, function (d) { return d.y });

			var scaleX = d3.scale.linear().domain([minX, maxX]).range([ 0, width - margin.right*2 ]);
			var scaleY = d3.scale.linear().domain([minY, maxY]).range([0, 20]);

			var timeline = d3.select('#timeline').append('svg').append("g");

			timeline.attr("transform", "translate(" + margin.right + "," + margin.top + ")");

			timeline.selectAll(".dot")
				.data(data)
				.enter().append("circle")
				.attr('class', 'dot')
				.attr("cx", function(d) { return scaleX(d.x); })
				.attr("cy", function(d) { return scaleY(d.y); })
				.attr("data-time", function(d) { return d.x; })
				.attr("r", 4);


			// Behaviors

			$('#map').on('click', 'path', function() {
				oo.filt.trigger( oo.filt.events.add, {'place':['Paris']} );
			});

			$('#timeline').on('click', 'circle', function() {
				var time = $(this).attr('data-time');
				oo.log(time)
				oo.filt.trigger( oo.filt.events.add, {'time':[time]} );
			});

	});
}


