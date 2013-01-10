var oo = oo || {};

oo.enq = {};
oo.enq.map = {};
oo.enq.timeline = {};
oo.enq.types = {};
oo.enq.docs = {};

var circleSize = {
	'small' : 2,
	'medium' : 10
};

// 
// 
// Enquête
// 
// 

oo.enq.init = function(){
	oo.filt.on( oo.filt.events.init, function( event, data ){
		oo.log("[oo.enq.init]");
		oo.enq.map.init( data.objects );
		oo.enq.timeline.init( data.objects );
		oo.enq.types.init( data.objects );
		oo.enq.docs.init( data.objects );
	});
}






