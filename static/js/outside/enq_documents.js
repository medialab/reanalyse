
// 
// Documents
// 
// 

oo.enq.docs.update = function( event, filters ){

	oo.log("[oo.enq.docs.update]");

	var	meter = 0;


	// Copy old status
	
	oo.enq.docs.li.each(function(d, i) {
		item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	});


	// Set new status
	
	for ( var i in oo.filt.data ) {
		
		var item = oo.enq.docs.ul.select('[data-id="' + oo.filt.data[i].id + '"]');

		if ( oo.filt.data[ i ].filtered ) {
			item.attr('data-status', 'active');
			meter++;
		} else {
			item.attr('data-status', 'inactive');	
		}

	}

	// oo.log('oo.filt.data', oo.filt.data)


	// Hide / Show Itemss

	oo.enq.docs.li.each(function() {

		var item = d3.select(this),
			oldStatus = item.attr('data-status-old'),
			newStatus = item.attr('data-status');

		if ( oldStatus == 'inactive' && newStatus == 'active' ) {
			item.style('display', 'block');
		} else if ( oldStatus == 'active' && newStatus == 'inactive' ) {
			item.style('display', 'none');
		}

	})

	// Update Counter

	if ( meter != oo.enq.docs.counter.attr('data-previous') ) {

		var delay = 800;

		oo.enq.docs.container.transition()
			.duration(delay / 2)
			.style('margin-top', '35px');

		oo.enq.docs.counter.transition()
			.duration(1)
			.delay(delay)
			.text( meter + '/' + oo.enq.docs.counter.attr('data-total') )
			.attr('data-previous', meter);
			
		oo.enq.docs.container.transition()
			.delay(delay * 1.2)
			.duration(delay)
			.style('margin-top', '0px');

	}


};





oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	oo.enq.docs.counter = d3.select('#counter span.docNumber');
	oo.enq.docs.ul = d3.select('#documents ul');
	oo.enq.docs.container = d3.select('#counter p');

	var map = objects.sort(function (a, b){ 
		return a.title > b.title ? 1 : a.title < b.title ? -1 : 0
	})

	// Set Reset Button

	d3.select("#reset").on("click", function() {
		
		// Reset categories
		d3.selectAll('#phases g, #categories g, #articles g').attr('data-status', 'normal');
		
		// Reset Map
		oo.enq.map.map.extent(layer.extent());

		// Reset Filters
    	oo.filt.clean();

    });

	// Create Documents

	oo.enq.docs.li = oo.enq.docs.ul.selectAll("li")
		.data(map)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.attr('data-status', 'active')
		
		.html(function(d) {
			var string = d.title + ' <small>('+d.type+')</small> <br/>';
			if (typeof d.date != 'undefined' ) string += '<i>' + d.date.substring(5, 7) + '/' + d.date.substring(0, 4) + '</i>' 
			if (typeof d.coordinates.properties.name != 'undefined' ) string += '<i>'+d.coordinates.properties.name+'</i>' 
			return string;
		})

		.on('click', function(d, i) {
			window.open( oo.api.urlfactory( oo.urls.get_document, d3.select(this).attr('data-id') ), '_blank');
			
			/*var string = d.title + ' <small>('+d.type+')</small> <br/>';
       		$( "#tabs" ).tabs( "add", "#tabs-2", string);

			( "#tabs" ).tabs('refresh')*/
			
		});

	// Set Documents' Counter

	oo.enq.docs.counter.text( oo.enq.docs.li[0].length + '/' + oo.enq.docs.li[0].length)
		.attr('data-total', oo.enq.docs.li[0].length)
		.attr('data-previous', oo.enq.docs.li[0].length);

	oo.enq.docs.container.transition()
		.duration(500)
		.style('margin-top', '0px');
	
	$('#documents-inner').slimScroll({height:600, color:'white'});
};

