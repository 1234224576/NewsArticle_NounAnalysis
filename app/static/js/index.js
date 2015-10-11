window.onload = function(){
	$('#loading').hide();
	$('#result').hide();

	var offsetX = 40;
	var offsetY = 20;
	var width = 400;
	var height = 350;

	var xScale = d3.scale.log()
	    .domain([1,7674])
	    .range([0,width]);
 
	var yScale = d3.scale.log()
        .domain([1000,1])
        .range([0,height]);

	d3.json("http://127.0.0.1:5000/frequencyrank?genre=all", function(data){
		drawGraph("#graph_all",data)
	});
	d3.json("http://127.0.0.1:5000/frequencyrank?genre=soci", function(data){
		drawGraph("#graph_soci",data)
	});
	d3.json("http://127.0.0.1:5000/frequencyrank?genre=pol", function(data){
		drawGraph("#graph_pol",data)
	});
	d3.json("http://127.0.0.1:5000/frequencyrank?genre=spo", function(data){
		drawGraph("#graph_spo",data)
	});
	function drawGraph(id,data){
		var circleElements = d3.select(id)
	 	.selectAll("circle")
	 	.data(data)
	 	.enter()
	 	.append("circle")
	 	.attr("class","mark")
	 	.attr("cx",function(d,i){
	 		return xScale(i+1) + offsetX;
	 	})
	 	.attr("cy",function(d,i){
	 		return yScale(d["sum"]) + offsetY;
	 	})
	 	.attr("r",2.0)

	 	function drawScale(id){
	 		d3.select(id)
	 			.append("g")
	 			.attr("class","y axis")
	 			.attr("transform","translate("+(offsetX)+"," + (offsetY) + ")")
	 			.call(
	 				d3.svg.axis()
	 				.scale(yScale)
	 				.orient("left")
	 				.ticks(10, 0)
	 			)
	 		d3.select(id)
	 			.append("g")
	 			.attr("class","x axis")
	 			.attr("transform","translate("+(offsetX)+"," + (height+offsetY) + ")")
	 			.call(
	 				d3.svg.axis()
	 				.scale(xScale)
	 				.orient("bottom")
	 				.ticks(10, 0)
	 			)
		}
		drawScale(id);
	}

    var start = 0;
    var tfidfData;
	$('#searchButton').on('click',function(){
		$("#tfidf_graph").empty();
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/tfidfrank?keyword="+$('#searchKeyword').val(),
            dataType: "json",
            success: function(res){
            	start = 0;
            	tfidfData = res;
            	$('#hitArticle').html(makeHtmlWithHitArticleData(res));
            	drawTfidfRankingGraph(tfidfData,start)
            	$('#loading').hide();
				$('#result').show();
            }
        });
    });

    function makeHtmlWithHitArticleData(res){
    	var html = "";
    	var article = {};
    	for(var i=0;i<res.length;i++){
    		if(!(res[i]["title"] in article)){
    			article[res[i]["title"]] = res[i]["content"];
     		}
    	}
    	for (var key in article) {
		 	 html += "<p>";
    		html += key;
    		html += "</p>";
		}
		$("#hitArticleButton").html("ヒットした記事（"+Object.keys(article).length+"件）")
    	return html;
    }


	$('#next').on('click',function(){
    	if(tfidfData.length > start+20){
    		start += 20;
    	}
    	$("#tfidf_graph").empty();
    	drawTfidfRankingGraph(tfidfData,start);
    });
    $('#back').on('click',function(){
    	if(start >= 20){
    		start -= 20;
    	}
    	$("#tfidf_graph").empty();
    	drawTfidfRankingGraph(tfidfData,start);
    });

    function drawTfidfRankingGraph(data,start){
		var offsetX = 120;
		var offsetY = 10;
		var width = 600;
		var height = 550;
		var xScale = d3.scale.linear()
	    	.domain([0,0.5])
	    	.range([0,450]);
	    var tfidf_graph;
		tfidf_graph = d3.select("#tfidf_graph")
		    .selectAll("rect")
		    .data(selectData(data,start));
		tfidf_graph.enter()
		    .append("rect")
		    .attr("x",offsetX)
		    .attr("y",function(d,i){
		      return i * 25 + offsetY;
		    })
		    .attr("height","20px")
		    .attr("width",function(d,i){
		      return xScale(d["tfidf"])+ "px";
		    });
		tfidf_graph.enter()
		 	.append("text")
		 	.attr("y",function(d,i){
		 		return i * 25 + offsetY + (25/2.0)+ "px";
		 	})
		 	.attr("x",20)
		 	.text(function(d,i){
		 		return d["noun"];
		 	});

	  	d3.select("#tfidf_graph")
	   		.append("g")
	    	.attr("class","x axis")
	    	.attr("transform","translate("+offsetX+","+ (height-offsetY-25) +")")
	   		.call(d3.svg.axis()
	      		.scale(xScale)
	      		.orient("bottom")
	    	)
	}

	function selectData(data,start){
		var rangeRank = 20;
		var selectData = [];
		for(var i=0;i<rangeRank;i++){
			if(data[start + i] != undefined) selectData[i] = data[start + i];
		}
		d3.select("#tfidf_graph").selectAll('*').remove();
		return selectData;
	}
}


