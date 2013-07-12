
// 
// Types
// 
// 





oo.Gummy = function ( objects, nester, selector, propertyName ){

	var types = d3.select( '#' + selector ),
		svg = types.append('svg').attr('width', 700),
		map = oo.nest( objects, 
			nester, 
			function (a, b){ return a.values.length < b.values.length ? 1 : a.values.length > b.values.length ? -1 : 0 }
		),
		width = types.style('width').slice(0, -2) - types.style('padding-left').slice(0, -2) * 2,
		sum = d3.sum(map, function(d) { return d.values.length }),
		gOrigin = 0,
		gHeight = 10;

	this.init = function(){

		oo.log("[oo.enq." + propertyName + ".init]");

		var scaleX = d3.scale.linear()
			.domain([ 0, sum ])
			.range([ 0,  width ]);

		for (var i in map) {
			
			var gWidth = scaleX( map[i].values.length );

			var	g = svg.append('g')
				.attr('data-id', map[i].key)
				.attr('data-status', 'normal')
				.attr('data-width', gWidth)
				.attr('data-origin', gOrigin)
				.attr('data-total', map[i].values.length)
				.attr('transform', 'translate(' + gOrigin + ', 0)')
				.attr('rel', 'tooltip')
				.attr('data-original-title', selector + '<div class="white"></div>' + map[i].values.length + '/' + map[i].values.length + ' of ' + map[i].key)

				.on("click", function() {

					d3.select('.tooltip').remove();
					
					var g = d3.select(this),
						obj = {},
						name = propertyName;

					oo.log('***', this)

					if ( g.attr('data-status') == 'normal' ) {

						types.selectAll('g').attr('data-status', 'hidden');
						g.attr('data-status', 'full'); // Set status
						obj[name] = g.attr('data-id');
						oo.filt.trigger( oo.filt.events.replace, obj ); // Send request

					} else {

						types.selectAll('g').attr('data-status', 'normal'); // Set status
						obj[name] = '';
						oo.filt.trigger( oo.filt.events.reset, '' ); // Send request

					}
				});

			g.append('rect')
				.attr('class', 'background')
				.attr('width', gWidth)
				.attr('height', gHeight)

			g.append('rect')
				.attr('class', 'percentage')
				.attr('width', gWidth - 1)
				.attr('height', gHeight)

			g.append('rect')
				.attr('class', 'line')
				.attr('transform', 'translate(0, ' + gHeight + ')')
				.attr('width', 1)
				.attr('height', 5)

			g.append('text')
				.attr('class', 'figure')
				.attr('width', gWidth)
				.attr('height', gHeight)
				.attr('transform', 'translate(0,25)')
				.text(gWidth < 60 ? map[i].values.length : map[i].values.length + ' ' + map[i].key)

			gOrigin += gWidth;

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
			    if ( map[i].key == gType ) { var gNumberPartial = map[ i ].values.length; }
			}

			// Set variables

			var g = d3.select(this),
			    gNumber = g.attr('data-total'),
			    gWidth = g.attr('data-status') == 'full' ? width : g.attr('data-width'),
			    gOrigin = g.attr('data-status') == 'full' ? 0 : g.attr('data-origin'),
				gScale = d3.scale.linear()
					.domain([ 0, gNumber ])
					.range([ 0,  gWidth ]),
				gWidthPartial = gScale(gNumberPartial),
				gText = gWidth < 60 ? gNumberPartial : gNumberPartial + ' ' + gType;

			// oo.log('g', g)
			// oo.log('gType', gType)
			// oo.log('gText', gText)
			// oo.log('gNumber', gNumber, 'gNumberPartial', gNumberPartial)
			// oo.log('gScale', gScale)
			// oo.log('gWidth', gWidth, 'gWidthPartial', gWidthPartial)

			g.attr('data-original-title', selector + '<div class="white"></div>' + gNumberPartial + '/' + gNumber + ' of ' + gType);

			if ( g.attr('data-status') == 'normal' || g.attr('data-status') == 'full' ) {

				g.transition()
					.duration(1000)
					.style('opacity', '1')
					.style('display', 'block')
					.attr('transform', 'translate(' + gOrigin + ', 0)');

				g.select('rect.percentage')
					.transition()
					.duration(1000)
					.attr( 'width', gWidthPartial - 1 < 0 ? 0 : gWidthPartial - 1 ) // Manage negative numbers

				g.select('rect.background')
					.transition()
					.duration(1000)
					.attr( 'width', gWidth ) // Manage negative numbers

				g.select('text.figure')
					.text(gText)

			} else if ( g.attr('data-status') == 'hidden' ) {
				g.transition()
					.duration(500)
					.style('opacity', '0')
					.each('end', function() {
						d3.select(this).style('display', 'none');
					});
			}

		});

	};

	this.init();

	oo.filt.on( oo.filt.events.change, this.update );

};





oo.enq.types.init = function(objects) {
	var categor1 = new oo.Gummy(objects, function( d ){
		return d.phases[0].phase;
	}, 'phases', 'phase');
	var categor2 = new oo.Gummy(objects, function( d ){ 
		return d.categories[0].category;
		// return d.categories.length > 0 ? d.categories[0].category : null;
	}, 'categories', 'category');
	var categor3 = new oo.Gummy(objects, function( d ){
		// return d.articles[0].article;
		return d.articles.length > 0 ? d.articles[0].article : null;
	}, 'articles', 'article');
}












