
// 
// Documents
// 
// 

oo.enq.docs.update = function( event, filters ){

	oo.log("[oo.enq.docs.update]");

	var docs = d3.select('#documents');

	var items = docs.selectAll('li').each(function(d, i) {
		item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	var counter = 0;

	for ( var i in oo.filt.data ) {
		var item = docs.select('li[data-id="' + oo.filt.data[i].id + '"]');
		if ( oo.filt.data[ i ].filtered ) {
			item.attr('data-status', 'active');
			counter++;
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

	d3.select('#counter').html(counter);
	
};

oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	var container = d3.select('#right-sidebar'),
		docs = container.select('#documents');

	var li = docs.selectAll("li")
		.data(objects)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.attr('data-status', 'active')
		.html(function(d) { return d.title.split('_').join(' ').split('/').join(' '); });

	var counter = container.append('div').attr('id', 'counter').html(li[0].length);
	
};

