
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


	items.each(function() {

		var item = d3.select(this),
			oldStatus = item.attr('data-status-old'),
			newStatus = item.attr('data-status');

		if ( oldStatus == 'active' && newStatus == 'inactive' ) {
			item.transition()
				.duration(1000)
				.style('opacity', '0')
				.style('height', '0px');
		} else if ( oldStatus == 'inactive' && newStatus == 'active' ) {
			item.transition()
				.duration(1000)
				.style('opacity', '1')
				.style('height', '22px');
		} 
	})

	var delay = 500;

	container.transition()
		.duration(delay)
		.style('margin-top', '24px');

	counter.transition()
		.duration(1)
		.delay(delay)
		.text(meter);
		
	container.transition()
		.delay(delay + 300)
		.duration(1000)
		.style('margin-top', '0px');

};

oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	var counter = d3.select('#counter span.docNumber'),
		docs = d3.select('#documents ul'),
		container = d3.select('#counter p');

	var li = docs.selectAll("li")
		.data(objects)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.attr('data-status', 'active')
		.html(function(d) { return d.title.split('_').join(' ').split('/').join(' '); });

	counter.html(li[0].length);

	container.transition()
		.duration(500)
		.style('margin-top', '0px');
	
};

