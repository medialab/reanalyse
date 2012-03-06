var dd=null;
////////////////////////////////////////////////////
function buildD3_Graph_SpeakersAttributes(data,theId) {
	dd=data;
	var w = 650,
		h = 450,
		legendW = 100,
		dec = 12,
		catfill = d3.scale.category10();
	
	var vis = d3.select("#"+theId).append("svg:svg")
		.attr("width", w)
		.attr("height", h)
		.style("background","#F8F8F8"); 
	
	var force = d3.layout.force()
		.charge(-120)
		.linkDistance(50+50*Math.random())
		.nodes(data.nodes)
		.links(data.edges)
		.size([w, h])
		.start();
	
	////////////////////////////////////////// Fade
	function fadeOnElem(opacity) {
		return function(d, i) {
			// edges
			vis.selectAll(".edge")
				.transition()
				.style("opacity", opacity);
			vis.selectAll(".edgeid_"+d.catid)
				.transition()
				.style("opacity", 0.5);
			// nodes
			vis.selectAll(".node")
				.transition()
				.style("opacity", opacity);
			vis.selectAll(".catid_"+d.catid)
				.transition()
				.style("opacity", 1);
			
			if(opacity!=1) {
				vis.selectAll(".textlabs")
					.filter( function(g,i) { return g.category!='Speaker' && g.catid==d.catid; })
					.style("opacity", 1);
					//.style("display","visible");
			}
			else {
				vis.selectAll(".textlabs")
					.style("opacity", 0.1);
					//.style("display","none");
			}
		};
	};
	
	////////////////////////////////////////// Graph		
	var edge = vis.selectAll("line.edge")
		.data(data.edges)
		.enter().append("svg:line")
			.attr("stroke", function(d) { return catfill(d.target.category); }) // get color of attribute node
			.style("stroke-width", function(d) { return Math.sqrt(d.value); })
			.style("opacity",0.5)
			.attr("class", function(d) { return "edge edgeid_"+d.source.catid+" edgeid_"+d.target.catid; })
			.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	
	var node = vis.selectAll("circle.node")
		.data(data.nodes)
		.enter().append("svg:circle")
			.attr("cx", function(d) { return d.x;} )
			.attr("cy", function(d) { return d.y;} )
			.attr("r", function(d) { return d.category=='Speaker' ? 7 : 3 ; })
			.style("fill", function(d) { return d.category=='Speaker' ? d.color : catfill(d.category) ; })
			.style("stroke", function(d) { return d.category=='Speaker' ? "white" : 'black' ; })
			.attr("class", function(d) { return "node catid_"+d.catid; })
			.on("mouseover",function(d,i) {
/*
				 vis.append("svg:text")
				 	.attr("class","label")
					.attr("x", d.x+10 )
					.attr("y", d.y+5 )
					.attr("fill","black")
					.attr("text-anchor","left")
					.text( d.label );
*/
			})
			.on("mouseout",function(d,i) {
				//d3.selectAll(".label").remove();
			})
			.call(force.drag);
			
	var labels = vis.selectAll("textlabels")
		.data(data.nodes)
		.enter().append("svg:text")
			.attr("class","textlabs")
			//.style("display","none")
			.style("opacity", 0.1)
			.attr("x", function(d) {return d.x+10 ; })
			.attr("y", function(d) {return d.y+5; })
			.attr("fill","black")
			.attr("text-anchor","left")
			.text( function(d) {return d.label;} );
			
	///////////////////////////////////// Legend
	vis.append("svg:rect")
		.attr("width",legendW)
		.attr("height",h)
		.attr("fill","white")
		.style("opacity",0.7);
	vis.append("svg:line")
		.attr("x1",legendW)
		.attr("x2",legendW)
		.attr("y1",0)
		.attr("y2",h)
		.attr("stroke","lightgray");
	var legend = vis.selectAll("legend")
		.data(data.legend);
	legend.enter().append("svg:circle")
		.attr("cx", function(d,i){ return d.category=='Speaker' ? 7 : legendW+10 ;})
		.attr("cy", function(d,i){ return d.category=='Speaker' ? 8+dec*(i-data.nattributes) : 8+dec*i })
		.attr("r", function(d,i){ return d.category=='Speaker' ? 5 : 3 ; })
		.style("fill", function(d) { return d.category=='Speaker' ? d.color : catfill(d.category) ; })
		.style("stroke", function(d) { return d.category=='Speaker' ? "none" : 'black' ; })
		.style("cursor","hand")
		.attr("class", function(d) { return "node catid_"+d.catid; });
	legend.enter().append("svg:text")
		.attr("x", function(d,i){ return d.category=='Speaker' ? 17 : legendW+25 ;})
		.attr("y", function(d,i){ return d.category=='Speaker' ? 8+dec*(i-data.nattributes)+4 : 8+dec*i+4 })
		.attr("text-anchor","left")
		.attr("fill","black")
		.attr("class", function(d) { return "node catid_"+d.catid; })
		.style("cursor","hand")
		.text(function(d) {return d.label;} )
		.on("mouseover", fadeOnElem(0.05))
		.on("mouseout", fadeOnElem(1));

		
/*
	vis.style("opacity", 1e-6)
		.transition()
		.duration(1000)
		.style("opacity", 1);
*/
	
	force.on("tick", function() {
		edge.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
			
		node.attr("cx", function(d) { return d.x;} )
			.attr("cy", function(d) { return d.y;} )
			
		labels.attr("x", function(d) { return d.x+10;} )
			.attr("y", function(d) { return d.y+5;} )
	});
};
