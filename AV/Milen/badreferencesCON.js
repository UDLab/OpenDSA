$(document).ready(function() {
  "use strict";
  var av_name = "badreferencesCON";
  var av = new JSAV(av_name)
  var xPosition = 400;
  var yPositionR1 = 10;
  var length1 = 100;
  var width = 30;

  av.g.rect(xPosition, yPositionR1, length1, width);
  //creating the x's
  av.g.line(xPosition + 10, yPositionR1 + 25, xPosition + 30, yPositionR1 + 3, {"stroke-width": 2});
  av.g.line(xPosition + 10, yPositionR1 + 3, xPosition + 30, yPositionR1 + 25, {"stroke-width": 2});

  av.g.line(xPosition + 40, yPositionR1 + 25, xPosition + 60, yPositionR1 + 3, {"stroke-width": 2});
  av.g.line(xPosition + 40, yPositionR1 + 3, xPosition + 60, yPositionR1 + 25, {"stroke-width": 2});

  av.g.line(xPosition + 70, yPositionR1 + 25, xPosition + 90, yPositionR1 + 3, {"stroke-width": 2});
  av.g.line(xPosition + 70, yPositionR1 + 3, xPosition + 90, yPositionR1 + 25, {"stroke-width": 2});

  //Slide 1
  av.umsg("This object would be seen as a bad reference.");
  av.displayInit();
  av.recorded();
});