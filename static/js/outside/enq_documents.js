
// 
// Documents
// 
// 

oo.enq.docs.update = function( event, filters ){

	oo.log("[oo.enq.docs.update]");

	var docs = d3.select('#documents');

	var items = docs.selectAll('li').each(function() {
		item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	for( var i in oo.filt.data ){
		if ( oo.filt.data[ i ].filtered == true ) {
			docs.select('li[data-id="' + oo.filt.data[i].id + '"]').attr('data-status', 'active');
		} else {
			docs.select('li[data-id="' + oo.filt.data[i].id + '"]').attr('data-status', 'inactive');
		}
	} // Set active

	items.each(function() {

		var item = d3.select(this);

		if ( (item.attr('data-status-old') == 'active') && (item.attr('data-status') == 'inactive') ) {
			item.transition()
				.duration(1000)
				.style('opacity', '0')
				.style('height', '0px');
		} else if ( (item.attr('data-status-old') == 'inactive') && (item.attr('data-status') == 'active') ) {
			item.transition()
				.duration(1000)
				.style('opacity', '1')
				.style('height', '22px');
		} 
	})
	
};

oo.enq.docs.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.docs.update );

	var docs = d3.select('#documents');

	docs.selectAll("li")
		.data(objects)
		.enter().append("li")
		.attr('class', 'active')
		.attr('data-id', function(d) { return d.id; })
		.attr('data-status', 'active')
		.html(function(d) { return d.title.split('_').join(' ').split('/').join(' '); });

};

