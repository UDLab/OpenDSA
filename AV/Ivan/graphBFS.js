"use strict";
/*global alert: true, ODSA */
$(document).ready(function() {

  var av = new JSAV("graphBFS");
  var g;
  var arr;
  var a, b, c, d, e, f;
  var firstElement;
  var lastElement;

  g = av.ds.graph({width: 500, height: 360, layout: "manual", directed: true});
  arr = av.ds.array(["","","","","",""],  {left: 600, top: 125});
  firstElement = 0;
  lastElement = 0;
  initGraph();
  g.layout();
  av.umsg("Let's look at the details of how a breadth-first seach works.");
  av.displayInit();
  markIt(g.nodes()[0]);
  av.step();
  bfs(g.nodes()[0]);
  finalGraph();
  av.recorded();


// Mark the nodes when visited and highlight it to
// show it has been marked
function markIt(node) {
  node.addClass("marked");
  av.umsg("Mark and enqueue " + node.value());
  arr.value(lastElement, node.value());
  lastElement++;
  node.highlight();
}

function dequeueIt(node) {
  node.addClass("dequeued");
  av.umsg("Dequeue " + node.value());
  arr.value(firstElement, "");
  firstElement++;
}

function bfs(start) {
  console.log("start : " + start.value());
  var node;
  var adjNode = new Array();
  var q = new Array();
  q.push(start);



 while(q.length > 0) {
    node = q.shift();
      dequeueIt(node);
    console.log("node " + node.value());
    adjNode = node.neighbors();
    console.log("adjNode " + adjNode.length);
    av.step();
    while(adjNode.length > 0) {

      if(!adjNode[0].hasClass("marked")) {
        markIt(adjNode[0]);
        av.step();
        adjNode[0].edgeFrom(node).addClass("markpath");
        av.step();
        q.push(adjNode[0]);
        adjNode.shift();
        console.log("adjNode after pop " + adjNode[0]);
      } else {
          adjNode.shift();
        }
    }
 }

}
function about() {
  alert("Breadth first search visualization");
}


// Graph prepartion for initial stage of visualization

function initGraph() {
  a = g.addNode("A", {"left": 25});
  b = g.addNode("B", {"left": 325});
  c = g.addNode("C", {"left": 145, "top": 75});
  d = g.addNode("D", {"left":145, "top": 200});
  e = g.addNode("E", {"top": 300});
  f = g.addNode("F", {"left":325, "top":250});
  g.addEdge(a, c);
  g.addEdge(a, e);
  g.addEdge(c, e);
  g.addEdge(c, b);
  g.addEdge(c, d);
  g.addEdge(c, f);
  g.addEdge(b, f);
  g.addEdge(d, f);
  g.addEdge(e, f);
  av.umsg("Initial call to BFS on A.");
}

// Resulting graph of completed depth first search
function finalGraph() {
  av.umsg("Completed breadth first search graph");
  g.removeEdge(e, f);
  g.removeEdge(d, f);
  g.removeEdge(b, f);
  g.removeEdge(f, e);
  g.removeEdge(f, d);
  g.removeEdge(f, b);
  g.removeEdge(c, e);

}
});
