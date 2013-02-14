
// 
// Types
// 
// 





oo.Gummy = function ( objects, selector, nester, propertyName ){

	var gummy = this;

	var types = d3.select( selector );

	
	var	svg = types.append('svg');
		var map = oo.nest( objects, 
			nester, 
			function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
		);

		var width = types.style('width').slice(0, -2) - types.style('padding-left').slice(0, -2) * 2,
		sum = d3.sum(map, function(d) { return d.values.length }),
		xPosition = 0,
		height = 10;

	this.init = function(){

		oo.log("[oo.enq." + propertyName + ".init]");

		var scaleX = d3.scale.linear()
			.domain([ 0, sum ])
			.range([ 0,  width ]);
			

		for (var i in map) {
			
			var gWidth = scaleX( map[i].values.length );

			var	g = svg.append('g')
				.attr('data-id', map[i].key)
				.attr('data-filter', 'false')
				.attr('data-width', gWidth)
				.attr('data-origin', xPosition)
				.attr('data-total', map[i].values.length)
				.attr('data-partial', map[i].values.length)
				.attr('transform', 'translate(' + xPosition + ', 0)')
				.attr('rel', 'tooltip')
				.attr('data-original-title', map[i].key)

				.on("click", function() {

					var g = d3.select(this);

					if ( g.attr('data-filter') == 'false' ) {

						// Set select status
						g.attr('data-filter', 'true');

						// Hide others
						// types.selectAll('g[data-filter=false]')
						// 	.transition()
						// 		.duration(500)
						// 		.style('opacity', '0')
						// 	.each('end', function() {
						// 		d3.select(this).style('display', 'none');
						// 	});

						// // Move group
						// g.transition()
						// 	.delay(500)
						// 	.duration(1000)
						// 	.attr('transform', 'translate(0, 0)');

						// // Lengthen background
						// g.select('rect.background')
						// 	.transition()
						// 	.delay(500)
						// 	.duration(1000)
						// 	.attr('width', width)

						// // Lengthen percentage
						// var tempPartial = g.attr('data-partial'),
						// 	tempTotal = g.attr('data-total'),
						// 	tempScale = d3.scale.linear()
						// 		.domain([ 0, tempTotal ])
						// 		.range([ 0,  width ]),
						// 	partialWidth = tempScale( tempPartial );

						// g.select('rect.percentage')
						// 	.transition()
						// 	.delay(500)
						// 	.duration(1000)
						// 	.attr('width', partialWidth);

						// // Set text
						// g.select('text')
						// 	.transition()
						// 	.delay(500)
						// 	.duration(500)
						// 	.each('end', function() {
						// 		d3.select(this).text( partialWidth < 60 ? tempTotal : tempTotal + ' ' + g.attr('data-id') )
						// 	})

						// Send request
						var obj = {},
							name = propertyName,
							value = g.attr('data-id');
						obj[name] = value;

						oo.filt.trigger( oo.filt.events.replace, obj );

					} else {

						

						// var x = g.attr('data-originalX'),
						// 	totalWidth = g.attr('data-originalWidth'),
						// 	partialNumber = g.attr('data-partial'),
						// 	totalNumber = g.attr('data-total'),
						// 	scaleX = d3.time.scale()
						// 		.domain([ 0, totalNumber ])
						// 		.range([ 0,  totalWidth ]),
						// 	partialWidth = scaleX(partialNumber);

						// // Set group position
						// g.transition()
						// 	.duration(1000)
						// 	.attr('transform', 'translate(' + x + ', 0)')

						// // Shorten background
						// g.select('rect.background')
						// 	.transition()
						// 	.duration(1000)
						// 	.attr('width', totalWidth)

						// // Shorten percentage
						// g.select('rect.percentage')
						// 	.transition()
						// 	.duration(1000)
						// 	.attr('width', partialWidth -1)

						// Show others and set unselected status
						// types.selectAll('g[data-filter=false]')
						// 	.style('display', 'block')
						// 	.transition()
						// 		.delay(500)
						// 		.duration(1000)
						// 		.style('opacity', '1')
						// 	.each('end', function() {
						// 		g.attr('data-filter', 'false');								
						// 	});

						// Set select status
						g.attr('data-filter', 'false');

						// // Set text
						// g.select('text').text( partialWidth < 60 ? partialNumber : partialNumber + ' ' + g.attr('data-id') )

						// Send request
						var obj = {},
							name = propertyName;
							value = '';
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
				.attr('width', gWidth - 1)
				.attr('height', height)

			g.append('rect')
				.attr('class', 'line')
				.attr('transform', 'translate(0, ' + height + ')')
				.attr('width', 1)
				.attr('height', 5)

			g.append('text')
				.attr('class', 'figure')
				.attr('width', gWidth)
				.attr('height', height)
				.attr('transform', 'translate(0,25)')
				.text(gWidth < 60 ? map[i].values.length : map[i].values.length + ' ' + map[i].key)

			xPosition += gWidth;

		}
	};


	this.update = function( event, filters ){

		oo.log("[oo.enq." + propertyName + ".update]");

		map = oo.nest( oo.filt.data, 
			nester, 
			function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
		);

		types.selectAll('g').each( function(){

			// Nest

			var gType = d3.select(this).attr('data-id');
			
			for (var i in map) {
			    if ( map[i].key == gType ) {
			    	var gNumberPartial = map[ i ].values.length;
			    }
			}

			// Set variables

			var g = d3.select(this),
			    gNumber = g.attr('data-total'),
			    gWidth = g.attr('data-filter') == 'true' ? width : g.attr('data-width'),
			    gOrigin = g.attr('data-filter') == 'true' ? 0 : g.attr('data-origin'),
				gScale = d3.scale.linear()
					.domain([ 0, gNumber ])
					.range([ 0,  gWidth ]),
				gWidthPartial = gScale(gNumberPartial),
				gText = gWidth < 60 ? gNumberPartial : gNumberPartial + ' ' + gType;

			oo.log('g', g)
			oo.log('gType', gType)
			oo.log('gText', gText)
			oo.log('gNumber', gNumber, 'gNumberPartial', gNumberPartial)
			oo.log('gScale', gScale)
			oo.log('gWidth', gWidth, 'gWidthPartial', gWidthPartial)

			g.transition()
				.duration(1000)
				.attr('transform', 'translate(' + gOrigin + ', 0)');

			g.select('rect.percentage')
				.transition()
				.duration(1000)
				.attr( 'width', gWidthPartial - 1 < 0 ? 0 : gWidthPartial - 1 ) // Manage negative numbers

			g.select('text.figure')
				.text(gText)

			// if 

			// types.selectAll('g[data-filter=false]')
			// 	.style('display', 'block')
			// 	.transition()
			// 		.delay(500)
			// 		.duration(1000)
			// 		.style('opacity', '1')
			// 	.each('end', function() {
			// 		g.attr('data-filter', 'false');								
			// 	});

			// types.selectAll('g[data-filter=false]')
			// 	.style('display', 'block')
			// 	.transition()
			// 		.delay(500)
			// 		.duration(1000)
			// 		.style('opacity', '1')
			// 	.each('end', function() {
			// 		g.attr('data-filter', 'false');								
			// 	});

			// types.selectAll('g[data-filter=false]')
			// 	.transition()
			// 		.duration(500)
			// 		.style('opacity', '0')
			// 	.each('end', function() {
			// 		d3.select(this).style('display', 'none');
			// 	});

		} )

	};

	this.init();

	oo.filt.on( oo.filt.events.change, this.update );

};





oo.enq.types.init = function(objects) {
	// var categor1 = new oo.Gummy(objects, '#phases', function( d ){ return d.phases[0].phase }, 'phase');
	// var categor2 = new oo.Gummy(objects, '#categories', function( d ){ 
	// 		return d.categories.length > 0? d.categories[0].category : null;
	// 	}, 'category');
	// var categor3 = new oo.Gummy(objects, '#articles', function( d ){
	// 		return d.articles.length > 0? d.articles[0].article : null;
	// 	}, 'article');
}












