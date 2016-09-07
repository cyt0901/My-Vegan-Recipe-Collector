// get data through AJAX
$.get('/my_recipes.json', function(results) {
  var newResults = JSON.parse(results);

  var treeData = d3.stratify()
     .id(function(d) { return d.name; })
     .parentId(function(d) { return d.parent; })
     (newResults);

  // set the dimensions and margins of the diagram
  var margin = {top: 100, right: 50, bottom: 70, left: 50},
    width = window.innerWidth - margin.right - margin.left,
    height = window.innerHeight - margin.top - margin.bottom,
    i = 0,
    duration = 300;

  // append the svg object to the body of the page
  // appends a 'group' element to 'svg'
  // moves the 'group' element to the top left margin
  var svg = d3.select(".my-contents").append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

  var defs = svg.append("defs").attr("id", "imgdefs");

  var circularPath = defs.append("clipPath").attr("id", "rec-circle")
                  .append("circle")
                    .attr("r", 58)
                    .attr("cy", 20)
                    .attr("cx", 5);

  var circularPath2 = defs.append("clipPath").attr("id", "main-circle")
                  .append("circle")
                    .attr("r", 85)
                    .attr("cy", 10)
                    .attr("cx", 0);


  //create path for curved lines connecting nodes
  var curvedLine = function(d) {
    return "M" + d.x + "," + d.y
       + "C" + (d.x + d.parent.x) / 2 + "," + d.y
       + " " + (d.x + d.parent.x) / 2 + "," +  d.parent.y
       + " " + d.parent.x + "," + d.parent.y;
  }

  //function to wrap label names of nodes
  var wrap = function(text, width) {
    text.each(function() {
      var text = d3.select(this);
      var words = text.text().split(/\s+/).reverse();
      var word;
      var line = [];
      var lineNumber = 0;
      var lineHeight = 1.1;
      var y = text.attr("y");
      var dy = parseFloat(text.attr("dy"));
      var tspan = text.text(null)
              .append("tspan")
              .attr("x", 0)
              .attr("y", y)
              .attr("dy", dy + "em");
      while (word == words.pop()) {
        line.push(word);
        tspan.text(line.join(" "));
        if (tspan.node().getComputedTextLength() > width) {
          line.pop();
          tspan.text(line.join(" "));
          line = [word];
          tspan = text.append("tspan")
              .attr("x", 0)
              .attr("y", y)
              .attr("dy", ++lineNumber * lineHeight + dy + "em")
              .text(word);
        }
      }
    });
  };

  // declares a tree layout and assigns the size
  var tree = d3.tree()
               .size([width, height]);

  //  assigns the data to a hierarchy using parent-child relationships
  var root = tree(d3.hierarchy(treeData));
  root.x0 = height / 2;
  root.y0 = 0;

  var collapse = function(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
  };

  //assign numerical ids
  root.each(function(d) {
    d.id = i;
    i += i;
  });

  //Start visualization with tree collapsed
  collapse(root);

  var update = function(source) {

    //new tree layout
    var nodes = tree(root).descendants();
    var links = nodes.slice(1);

    //normalize fixed-depth
    nodes.forEach(function(d) {
      d.y = d.depth * 200;
    });

    //update nodes
    var node = svg.selectAll("g.node")
          .data(nodes, function(d) {
            return d.id || (d.id += i);
          });

    //enter new nodes at parent's previous position
    var nodeEnter = node.enter().append("g")
        .attr("class", function(d) {
          if (d.children === null & d._children === null) {
            return "node node-recipe";
          } else {
            return "node node-label";
          }
        })
        .attr("transform", function() {
          return "translate(" + source.x0 + "," + source.y0 + ")";
        })
        .on("click", function(d) {
          if (d.children) {
            d._children = d.children;
            d.children = null;
          } else {
            d.children = d._children;
            d._children = null;
          }
          if (d.parent) {
            d.parent.children.forEach(function(element) {
              if (d !== element) {
                collapse(element);
              }
            });
          } else {
            console.log("ROOT");
          }
          if (d.children || d._children) {
            update(d);
          }
        });

    nodeEnter.filter(function(d) { return (d.data.data.url !== null); })
      .append("a")
        .attr("xlink:href", function(d) { return d.data.data.url; })
      .append("image")
        .attr("clip-path", "url(#rec-circle)");

    nodeEnter.filter(function(d) { return (d.data.data.url === null); })
      .append("image");

    nodeEnter.filter(function(d) { return (d.data.parent === null); })
      .select("image")
      .attr("clip-path", "url(#main-circle)");

    nodeEnter.select("image")
        .attr("xlink:href", function(d) { return d.data.data.img; })
        .attr("width", function(d) {
          var d_value = d.data.data.value;
          return d.data.data.url ? (d_value * 40) : (d_value * 30);
        })
        .attr("height", function(d) {
          var d_value = d.data.data.value;
          return d.data.data.url ? (d_value * 40) : (d_value * 30);
        })
        .attr("x", function(d) {
          return -(d.data.data.value * 15);
        })
        .attr("y", function(d) {
          return -(d.data.data.value * 15);
        });
      
    nodeEnter.append("text")
      .attr("dy", "0.5em")
      .attr("y", function(d) { return d.children || d._children ? 0 : 85; })
      .attr("text-anchor", "middle")
      .text(function(d) { return d.data.data.name; })
      .style("fill-opacity", 1e-6)
      .style("font-size", function(d) { return d.data.data.value * 5; })
      .style("opacity", function(d) {
        if (d.children || d._children) {
          return 1;
        } else {
          return 0;
        }
      })
      .call(wrap, 140);

    

    svg.selectAll(".node")
       .on("mouseenter", function () {
          if (this.attributes.class.value == "node node-recipe") {
            this.parentNode.appendChild(this);
          }
          d3.select(this).select("image").transition()
            .attr("width", function(d) {
              var d_value = d.data.data.value;
              return d.data.data.url ? (d_value * 50) : (d_value * 40);
            })
            .attr("height", function(d) {
              var d_value = d.data.data.value;
              return d.data.data.url ? (d_value * 50) : (d_value * 40);
            })
            .attr("x", function(d) {
              return -(d.data.data.value * 20);
            })
            .attr("y", function(d) {
              return -(d.data.data.value * 20);
            });
          if (this.attributes.class.value == "node node-recipe") {
            d3.select(this).select("text").transition()
              .style("opacity", 1);
          } else {
            d3.select(this).select("text")
              .style("font-size", function(d) {
                return d.data.data.value * 7;
              });
          }
        })
        .on("mouseleave", function() {
          d3.select(this).select("image").transition()
            .attr("width", function(d) {
              var d_value = d.data.data.value;
              return d.data.data.url ? (d_value * 40) : (d_value * 30);
            })
            .attr("height", function(d) {
              var d_value = d.data.data.value;
              return d.data.data.url ? (d_value * 40) : (d_value * 30);
            })
            .attr("x", function(d) {
              return -(d.data.data.value * 15);
            })
            .attr("y", function(d) {
              return -(d.data.data.value * 15);
            });
          if (this.attributes.class.value == "node node-recipe") {
            d3.select(this).select("text").transition()
              .style("opacity", 0);
          } else {
            d3.select(this).select("text")
              .style("font-size", function(d) {
                return d.data.data.value * 5;
              });
          }
        });

    //transition to new positions
    var nodeUpdate = node.merge(nodeEnter).transition()
      .duration(duration)
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });

    nodeUpdate.select("text")
      .style("fill-opacity", 1);

    //transition exiting nodes
    var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function() {
        return "translate(" + source.x + "," + source.y + ")";
      })
      .remove();

    nodeExit.select("text")
      .style("fill-opacity", 1e-6);

    //update links
    var link = svg.selectAll("path.link")
      .data(links, function(d) {
        return d.id;
      });

    link.transition()
      .duration(duration)
      .attr("d", curvedLine);

    var linkEnter = link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function() {
        var o = {x: source.x0, y: source.y0, parent: {x: source.x0, y: source.y0}};
        return curvedLine(o);
      });

    link.merge(linkEnter).transition()
      .duration(duration)
      .attr("d", curvedLine);

    link.exit().transition()
      .duration(duration)
      .attr("d", function() {
        var o = {x: source.x, y: source.y, parent: {x: source.x, y: source.y}};
        return curvedLine(o);
      })
      .remove();

    nodes.forEach(function(d) {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  };

  update(root);
});