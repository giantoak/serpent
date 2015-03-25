function handleFiles(files) {
	// Check for the various File API support.
	if (window.FileReader) {
		// FileReader are supported.
		getAsText(files[0]);
	} else {
		alert('FileReader are not supported in this browser.');
	}
}

function getAsText(fileToRead) {
	var reader = new FileReader();
	// Handle errors load
	reader.onload = loadHandler;
	reader.onerror = errorHandler;
	// Read file into memory as UTF-8      
	reader.readAsText(fileToRead);
}

function loadHandler(event) {
	var csv = event.target.result;
	processData(csv);             
}

function processData(csv) {
    var allTextLines = csv.split(/\r\n|\n/);
    var lines = [];
    while (allTextLines.length) {
        lines.push(allTextLines.shift().split('\t'));
    }
	
	drawOutput(lines);
}

function errorHandler(evt) {
	if(evt.target.error.name == "NotReadableError") {
		alert("Canno't read file !");
	}
}

function drawOutput(lines){
	//Clear previous data


	 $.ajax({
        type:"POST",
        url:"phone_app/geocode",
        contentType:'application/json',
        dataType:'json',
        crossDomain: true,
        data: JSON.stringify({'phone_list':lines}),
        success: function(data){
        	console.log(data)
        	data2=data['list']
         	document.getElementById("phonebook").innerHTML = "";
			var table = document.createElement("table");
			table.setAttribute('id','phone');
			for (var i = 0; i < data2.length; i++) {
				var row = table.insertRow(-1);
				for (var j = 0; j < data2[i].length; j++) {
					var firstNameCell = row.insertCell(-1);
					firstNameCell.appendChild(document.createTextNode(data2[i][j]));
				}
			}
		    //document.getElementById("phonebook").appendChild(table);

		    tbl_row=""
		    tbl_body=""
		    for (var i = 0; i < data2.length; i++) {
 			tbl_row+="<tr><td>"+data2[i][0]+"</td><td>"+data2[i][1]+"</td><td>"+data2[i][2]+"</td><td>"+data2[i][3]+"</td></tr>"
		    }
	

           tbl_body+='<table id="phone" class="display"><thead><tr><th>Source</th><th>Number</th><th>Contact</th><th>Location</th></thead><tbody>'+tbl_row+"</tbody></table>"
           $("#phonebook").html(tbl_body)
           $("#phone").dataTable();

       	   
function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}



 
			graph=data['graph']

			  var width = 1200,
			    height = 1000;
                        var country=graph['nodes'].map(function(x){return x.country});
			console.log(country.filter(onlyUnique))
      			var color = d3.scale.category20().domain(country.filter(onlyUnique))
                        console.log(color('Benin'))

			var svg = d3.select("#network").append("svg")
			    .attr("width", width)
			    .attr("height", height);

			 var force = d3.layout.force()
			    .nodes(graph.nodes)
			    .links(graph.links)
			    .size([width, height])
			    .linkDistance(60)
			    .charge(-150)
			    .start();

			  var link = svg.append("g").selectAll(".link")
			      .data(graph.links)
			    .enter().append("line")
			      .attr("class", "link");

			// Create the groups under svg
			var gnodes = svg.selectAll('g.gnode')
			  .data(graph.nodes)
			  .enter()
			  .append('g')
			  .classed('gnode', true);

			// Add one circle in each group
			var node = gnodes.append("circle")
			  .attr("class", "node")
			  .attr("r", 5)
			  .attr("fill",function(d){
			   return color(d.country)})
			  .call(force.drag);

			// Append the labels to each group
			var labels = gnodes.append("text")
			  .text(function(d) { return d.id; });

			force.on("tick", function() {
			  // Update the links
			  link.attr("x1", function(d) { return d.source.x; })
			    .attr("y1", function(d) { return d.source.y; })
			    .attr("x2", function(d) { return d.target.x; })
			    .attr("y2", function(d) { return d.target.y; });

			  // Translate the groups
			  gnodes.attr("transform", function(d) { 
			    return 'translate(' + [d.x, d.y] + ')'; 
			  });    

			});


		        }
	});

}
