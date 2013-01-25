
// 
// Types
// 
// 





oo.Gummy = function ( objects, selector, nester, propertyName ){

	var gummy = this;

	var types = d3.select( selector );

	this.init = function(){

		var map = oo.nest( objects, 
			nester, 
			function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
		)
		sum = d3.sum(map, function(d) { return d.values.length })
		width = types.style('width').slice(0, -2) - types.style('padding-left').slice(0, -2) * 2,
		scaleX = d3.scale.linear()
			.domain([ 0, sum ])
			.range([ 0,  width ]),
		svg = types.append('svg'),
		xPosition = 0,
		height = 10;

		for (var i in map) {
			
			var gWidth = scaleX( map[i].values.length ),

				g = svg.append('g')
					.attr('data-id', map[i].key)
					.attr('data-filter', 'false')
					.attr('data-originalWidth', gWidth)
					.attr('data-originalX', xPosition)
					.attr('data-total', map[i].values.length)
					.attr('data-partial', map[i].values.length)
					.attr('transform', 'translate(' + xPosition + ', 0)')

					.on("click", function() {

						var g = d3.select(this);

						if ( g.attr('data-filter') == 'false' ) {

							g.attr('data-filter', 'true');

							// Hide others
							types.selectAll('g[data-filter=false]')
								.transition()
								.duration(500)
								.style('opacity', '0');

							// Move group
							g.transition()
								.delay(500)
								.duration(1000)
								.attr('transform', 'translate(0, 0)');

							// Lengthen background
							g.select('rect.background')
								.transition()
								.delay(500)
								.duration(1000)
								.attr('width', width)

							// Lengthen percentage
							var tempPartial = g.attr('data-partial'),
								tempTotal = g.attr('data-total'),
								tempScale = d3.scale.linear()
									.domain([ 0, tempTotal ])
									.range([ 0,  width ]),
								partialWidth = tempScale( tempPartial );

							g.select('rect.percentage')
								.transition()
								.delay(500)
								.duration(1000)
								.attr('width', partialWidth);

							var obj = {};
							var name = propertyName;
  							var value = g.attr('data-id');
  							obj[name] = value;

							oo.filt.trigger( oo.filt.events.replace, obj );

						} else {

							var x = g.attr('data-originalX'),
								totalWidth = g.attr('data-originalWidth'),
								partialNumber = g.attr('data-partial'),
								totalNumber = g.attr('data-total'),
								scaleX = d3.time.scale()
									.domain([ 0, totalNumber ])
									.range([ 0,  totalWidth ]),
								partialWidth = scaleX(partialNumber);

							// Set group position
							g.transition()
								.duration(1000)
								.attr('transform', 'translate(' + x + ', 0)')

							// Shorten background
							g.select('rect.background')
								.transition()
								.duration(1000)
								.attr('width', totalWidth)

							// Shorten percentage
							g.select('rect.percentage')
								.transition()
								.duration(1000)
								.attr('width', partialWidth)

							// Show others
							types.selectAll('g[data-filter=false]')
								.transition()
								.delay(500)
								.duration(1000)
								.style('opacity', '1')
								.each("end", function() {
									g.attr('data-filter', 'false');
								})

							var obj = {};
							var name = propertyName;
  							var value = '';
  							obj[name] = value;

							oo.filt.trigger( oo.filt.events.reset, obj );

					}

				});

			g.append('rect')
				.attr('class', 'background')
				.attr('width', gWidth)
				.attr('height', height)

			g.append('rect')
				.attr('class', 'percentage')
				.attr('width', gWidth)
				.attr('height', height)

			g.append('rect')
				.attr('class', 'line')
				.attr('transform', 'translate(0, ' + height + ')')
				.attr('width', 1)
				.attr('height', 15)

			g.append('text')
				.attr('class', 'figure')
				.attr('width', gWidth)
				.attr('height', height)
				.attr('transform', 'translate(4,25)')
				.text(map[i].values.length + ' ' + map[i].key)

			xPosition += gWidth;

		}
	};


	this.update = function( event, filters ){

		oo.log("[oo.enq." + selector + ".update]");

		var map = oo.nest( oo.filt.data, 
			nester, 
			function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
		);

		var width = types.style('width').slice(0, -2) - types.style('padding-left').slice(0, -2) * 2;

		types.selectAll('g')
			.each( function(){

				var g = d3.select(this),
					type = g.attr('data-id'),
				    totalNumber = g.attr('data-total'),
				    totalWidth = g.attr('data-filter') == 'true' ? width : g.attr('data-originalWidth');

				for (var i in map) {
				    if (map[i].key == type) {
				    	var partialNumber = map[ i ].values.length;
				    }
				}

				var scaleX = d3.scale.linear()
						.domain([ 0, totalNumber ])
						.range([ 0,  totalWidth ]),
					partialWidth = scaleX(partialNumber);

				if ( g.attr('data-filter') == 'false' ) {
					g.select('rect.percentage')
						.transition()
						.duration(1000)
						.attr('width', partialWidth)				
				}

				g.select('text.figure')
					.text(partialNumber + ' ' + type)

				g.attr('data-partial', partialNumber);

			} )

	};

	this.init();

	oo.filt.on( oo.filt.events.change, this.update );

};





oo.enq.types.init = function(objects) {
	var categor1 = new oo.Gummy(objects, '#types', function( d ){ return d.type }, 'type');
	var categor2 = new oo.Gummy(objects, '#categories', function( d ){ return d.categories[0].category }, 'category');
	var categor2 = new oo.Gummy(objects, '#phases', function( d ){ return d.phases[0].phase }, 'phase');
}












