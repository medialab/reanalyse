////////////////////////////////////////////////////
function buildD3_StudyOverview(data,theId,param) {
	var unik = "#"+theId;
	var vizdiv = d3.select(unik).append("div")
		.style("border","1px solid gray")
		.style("width","100%")
		.style("height","200px");
	
	docs = data['documents'];
	
/*
	min_max_date = data.reduce(function (p, c) {
		// select max and min date
		return [
			(p[0] < c[_timestamp])? p[0]: c[_timestamp],
			(p[1] > c[_timestamp])? p[1]: c[_timestamp]
		];
	}
*/
        
	var rectdiv = vizdiv.append("svg:g")
		.attr("width",200)
		.attr("height",100);
	
/*
	rectdiv.selectAll('documents')
		.data(docs)
		.enter().append("svg:rect")
			.attr("width",20)
			.attr("height",30)
			.style("background","lightgray");
*/

	console.log("done");
};