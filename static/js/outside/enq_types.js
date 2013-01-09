
// 
// Types
// 
// 

oo.enq.types.update = function( event, filters ){

	oo.log("[oo.enq.types.update]");

	var items = d3.selectAll('#types li').each(function() {
		var item = d3.select(this);
		item.attr('data-status-old', item.attr('data-status'));
	}); // Copy new status to old status

	items.attr('data-status', 'inactive'); // Reset

	var map = {};
	for (var i in oo.filt.data) {
		j = oo.filt.data[i].type;
		if ( ( oo.filt.data[ i ].filtered.extent == 0 ) && ( oo.filt.data[ i ].filtered.period == 0 ) ) {
			if(map.hasOwnProperty(j)) { 
			    map[j]++;
			} else {
				map[j] = 1;
			}
		}
	}

	for( var i in map ){
		d3.select('#types li[data-id="' + i + '"]')
			.attr('data-status', 'active')
			.html(map[i] + ' ' + i);
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
				.style('height', '30px');
		}

	})
	
};

oo.enq.types.init = function ( objects ){

	oo.filt.on( oo.filt.events.change, oo.enq.types.update );

	var map = {};
	for (var i in objects) {
		j = objects[i].type;
		if(map.hasOwnProperty(j)) { 
		    map[j]++;
		} else {
			map[j] = 1;
		}
	}

	var types = d3.selectAll('#types');

	for (var i in map) {
		types.append('li')
		.attr('data-id', i)
		.attr('data-status', 'active')
		.html(map[i] + ' ' + i);
	}

};
