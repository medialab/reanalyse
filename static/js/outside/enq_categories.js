
// 
// Types
// 
// 

// type
// categories
// phases

oo.enq.types.update = function( event, filters ){

	oo.log("[oo.enq.types.update]");

	var map = oo.nest( oo.filt.data, 
		function( d ){ return d.type }, 
		function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
	);

	var width = d3.select("#types").style('width').slice(0, -2) - d3.select("#types").style('padding-left').slice(0, -2) * 2;

	var g = d3.selectAll('#types g')

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

			oo.log('totalWidth', totalWidth, 'totalNumber', totalNumber, 'partialNumber', partialNumber)

			var scaleX = d3.scale.linear()
				.domain([ 0, totalNumber ])
				.range([ 0,  totalWidth ]),
				partialWidth = scaleX(partialNumber);

			oo.log('partialWidth', partialWidth)

			if ( g.attr('data-filter') == 'false' ) {
				g.select('rect.percentage')
					.transition()
					// .delay(500)
					.duration(1000)
					.attr('width', partialWidth)				
			}


			g.select('text.figure')
				.text(partialNumber + ' ' + type)

			g.attr('data-partial', partialNumber);

		} )

};




oo.enq.types.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.types.update );

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
						d3.selectAll('#types g[data-filter=false]')
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

						oo.filt.trigger( oo.filt.events.replace, {'type': g.attr('data-id')} );

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
						d3.selectAll('#types g[data-filter=false]')
							.transition()
							.delay(500)
							.duration(1000)
							.style('opacity', '1')
							.each("end", function() {
								g.attr('data-filter', 'false');
							})


						oo.filt.trigger( oo.filt.events.reset, {'type': []} );

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


















