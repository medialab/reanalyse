
// 
// Documents
// 
// 

oo.enq.docs.update = function( event, filters ){

	oo.log("[oo.enq.docs.update]");

	var	docs = d3.select('#documents ul'),
		counter = d3.select('#counter span.docNumber')
		container = d3.select('#counter p'),
		meter = 0;

	var items = docs.selectAll('li').each(function(d, i) {
		item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	for ( var i in oo.filt.data ) {
		var item = docs.select('li[data-id="' + oo.filt.data[i].id + '"]');
		if ( oo.filt.data[ i ].filtered ) {
			item.attr('data-status', 'active');
			meter++;
		} else {
			item.attr('data-status', 'inactive');	
		}
	} // Set active


	// Hide / Show list's

	items.each(function() {

		var item = d3.select(this),
			oldStatus = item.attr('data-status-old'),
			newStatus = item.attr('data-status');

		if ( oldStatus == 'inactive' && newStatus == 'active' ) {
			item.style('display', 'block');
		} else if ( oldStatus == 'active' && newStatus == 'inactive' ) {
			item.style('display', 'none');
		}

	})

	var delay = 800;

	container.transition()
		.duration(delay / 2)
		.style('margin-top', '35px');

	counter.transition()
		.duration(1)
		.delay(delay)
		.text( meter + '/' + counter.attr('data-total') );
		
	container.transition()
		.delay(delay * 1.2)
		.duration(delay)
		.style('margin-top', '0px');

};

oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	var counter = d3.select('#counter span.docNumber'),
		total = d3.select('#counter span.docTotal'),
		docs = d3.select('#documents ul'),
		container = d3.select('#counter p'),
		map = objects.sort(function (a, b){ 
		return a.title > b.title ? 1 : a.title < b.title ? -1 : 0
	})

	// Set Reset Button

	d3.select("#reset").on("click", function() {
    	oo.filt.clean();
		oo.enq.map.map.extent(layer.extent());
    });

	// Create Documents

	var li = docs.selectAll("li")
		.data(map)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.attr('data-status', 'active')
		
		.html(function(d) {
			var string = d.title.split('_').join(' ').split('/').join(' ') + '<br/>';
			if (typeof d.type != 'undefined' ) string += '<i>'+d.type+'</i>' 
			if (typeof d.phases[0].phase != 'undefined' ) string += '<i>'+d.phases[0].phase+'</i>' 
			if (typeof d.categories[0].category != 'undefined' ) string += '<i>'+d.categories[0].category+'</i>' 
			if ( d.articles.length != 0 ) string += '<i>'+d.articles[0].article+'</i>' 
			return string;
		})

		.on('click', function(d, i) {
			oo.log('this', this)
			oo.log('id', d3.select(this).attr('data-id'))
			window.open( oo.api.urlfactory( oo.urls.get_document, d3.select(this).attr('data-id') ), '_blank');
		});

	// Set Documents' Counter

	counter.text(li[0].length + '/' + li[0].length)
		.attr('data-total', li[0].length);

	container.transition()
		.duration(500)
		.style('margin-top', '0px');
	
	$('#documents-inner').slimScroll({height:493});
};

