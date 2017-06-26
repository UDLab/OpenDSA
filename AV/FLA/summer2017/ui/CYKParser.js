$(document).ready(function () {
  var variables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var jsav = new JSAV("av");
  var inputString,
      productions,
      fi,
      oldrow,
      oldcol,
      table, //table with the answer
      userTable, //has the same value as jsavParseTable, but just for backend use
      jsavParseTable, //table that the user could see and input
      currentStep = 0; //for the step function

  var arrow = String.fromCharCode(8594),
      lambda = String.fromCharCode(955),
      epsilon = String.fromCharCode(949),
      square = String.fromCharCode(9633),
      dot = String.fromCharCode(183),
      emptystring = lambda;


  var productions = JSON.parse(localStorage.getItem('grammars'));
  var grammars = jsav.ds.matrix(productions, {style: "table"});
  grammars.layout();


  function enterInput() {
    inputString = prompt('Input string');
    if (inputString !== null) {
      cykParse();
    }
  }

  function cykParse() {
    // //first convert grammar to CNF, currently there seems to be problems with convertToChomsky()
    // var cnf = convertToChomsky();
    // console.log(cnf);

    if (productions.length === 0) {
      alert('No grammar.');
      return;
    }
    jsav.umsg('Please input your answer');

    // startParse();

    var inputLength = inputString.length;
    var nonterminals = getNonTerminals();
    var terminals = getTerminals();

    //initialize the 2d (3d) array
    // var table = new Array(inputLength);
    // for (var s = 0; s < inputLength; s++) {
    //   table[s] = new Array(inputLength);
    //   for(var i = 0; i < nonterminals.size; i++){
    //     table[s][i] = new Array(nonterminals.size);
    //   }
    // }

    //table will be the one with the correct answer, while userTable will be used for user to input, 
    //TODO: need to refactor this part
    table = new Array(inputLength);
    userTable = new Array(inputLength);
    for (var s = 0; s < inputLength; s++) {
      table[s] = new Array(inputLength-s);
      userTable[s] = new Array(inputLength-s);
      for(var i = 0; i < inputLength-s; i++){
        table[s][i] = new Array();
        userTable[s][i] = new Array();
      }
    }

    var unitProductions = _.filter(productions, function(x) {
      return x[2].length === 1 && variables.indexOf(x[2]) === -1;
    });
    //the first row, unit productions
    for (var s = 0; s < inputLength; s++) {
      unitProductions.forEach(function(production) {
        if(production[2] == inputString.charAt(s)){
          table[0][s].push(production[0]);
        }
      });
    }
    var otherProductions = _.filter(productions, function(x) {
      return x[2].length === 2;
    });
    for (var l = 2; l <= inputString.length; l++) { //l is length of the span
      for (var s = 0; s <= inputString.length - l; s++) {  //s is the start of the span
        e = s + l - 1; //e is the end of the span
        for (var p = s; p <= e - 1; p++) { //p is where the partition is
            otherProductions.forEach(function(production) {
              // other productions are in the form of A -> BC
              var A = production[0];
              var B = production[2].charAt(0);
              var C = production[2].charAt(1);
              if(table[p-s][s].includes(B) && table[l-p+s-2][p+1].includes(C)) {
                if(!table[l-1][s].includes(A)){
                  table[l-1][s].push(A);
                }
              }
            });
        }
      }
    }

    initCYKParseTable(userTable);
    checkAcceptance(table);

  };

  var checkAcceptance = function (table) {
    if(table[inputString.length - 1][0].length > 0) {
      alert('Input accepted');
    }else{
      alert('Input not accpeted');
    }
  }




  //initialize the parsetable
  var initCYKParseTable = function (table) {
      jsavParseTable = jsav.ds.matrix(table);
      layoutCYKParseTable();
      jsavParseTable.on('click', cykParseTableHandler);
  };

  //a special layout function for CYK parse table, shows only half of the matrix.
  function layoutCYKParseTable() {
    jsavParseTable.layout();
    for (var i = 0; i < jsavParseTable._arrays.length; i++) {
      var arry = jsavParseTable._arrays[i].element;
      arry.css({"width": "250px"}); //the width is currently hardcoded to ensure left align, need to change in the future
    }
  };
  
  //Set the values of the parse table accourding to the argument, instead of creating a new matrix
  function setCYKParseTable(table) {
    for(var r = 0; r < table.length; r++){
      for(var c = 0; c < table[r].length; c++){
        jsavParseTable._arrays[r].value(c, table[r][c]);
      }
    }
  }


  //for user interactions
  var cykParseTableHandler = function(row, col) {
      console.log(row + '  ' + col);
      if (fi) {
        var input = fi.val();
        //If user didn't input anything, and there already exists info in that cell, do nothing
        if (input === "" && userTable[oldrow][oldcol].length > 0) {
           input = userTable[oldrow][oldcol];
        }
        fi.remove();

        jsavParseTable.value(oldrow, oldcol, input);
        userTable[oldrow][oldcol] = input;
        layoutCYKParseTable(jsavParseTable);
        checkAnswer(oldrow, oldcol);
      }

      var offset = jsavParseTable._arrays[row]._indices[col].element.offset();
      var topOffset = offset.top;
      var leftOffset = offset.left;
      $('#firstinput').remove();
      var createInput = "<input type='text' id='firstinput' onfocus='this.value = this.value;'>";
      $('body').append(createInput);
      fi = $('#firstinput');
      fi.offset({top: topOffset, left: leftOffset});
      fi.outerHeight($('.jsavvalue').height());
      fi.width($(jsavParseTable._arrays[row]._indices[col].element).width());
      fi.focus();

      //need these in order to update the table correctly
      oldrow = row;
      oldcol = col;

  };

  //check the user input against the answer at a specific index
  function checkAnswer(row, col) {
    var correct = true;
    for(var i = 0; i < table[row][col].length; i++){
      if(!jsavParseTable.value(row, col).includes(table[row][col][i])){
        correct = false;
        break;
      }
    }
    if(!correct){
      jsavParseTable._arrays[row].css([col], {"color": "red"});
    } else {
      jsav.umsg('Please continue to input your answer');
      jsavParseTable._arrays[row].css([col], {"color": "green"});
      if(jsavParseTable.value(inputString.length - 1, 0).length > 0) {
      alert('Congratulations!');
        jsav.umsg('Accepted!');
      }
    }
  };

  //return a set of unique terminals on the right side
  function getTerminals() {
    // var productions = _.filter(arr, function(x) { return x[0]});
    var set = new Set();
    for (var i = 0; i < productions.length; i++) {
      var rhs = productions[i][2];
      for(var k = 0; k < rhs.length; k++){
        if(variables.indexOf(rhs.charAt(k)) === -1 && !(set.has(rhs.charAt(k)))) {
          set.add(rhs.charAt(k));
        }
      }
    }
    return set;
  }

  //return a set of unique variables (non-terminals) on the left side
  function getNonTerminals() {
    // var productions = _.filter(arr, function(x) { return x[0]});
    var set = new Set();
    for (var i = 0; i < productions.length; i++) {
      var lhs = productions[i][0];
      for(var k = 0; k < lhs.length; k++){
        if(variables.indexOf(lhs.charAt(k)) !== -1 && !(set.has(lhs.charAt(k)))) {
          set.add(lhs.charAt(k));
        }
      }
    }
    return set;
  }


  // fired when document is clicked
  // saves current fi input value
  function defocus(e) {
    if ($(e.target).hasClass("jsavvaluelabel")) return;
    if ($(e.target).attr('id') == "firstinput") return;
    if (!fi || !fi.is(':visible')) return;
    var input = fi.val();
    //If user didn't input anything, and there already exists info in that cell, do nothing
    if (input === "" && userTable[oldrow][oldcol].length > 0) {
      input = userTable[oldrow][oldcol];
    }
    fi.remove();
    jsavParseTable.value(oldrow, oldcol, input);
    userTable[oldrow][oldcol] = input;
    layoutCYKParseTable(jsavParseTable);
    checkAnswer(oldrow, oldcol);
  }

  function completeCYKTable(){
    setCYKParseTable(table);
  };

  function step(){
    if(currentStep < table.length){
      userTable[currentStep] = table[currentStep];
      setCYKParseTable(userTable);
      //show green
      for(var c = 0; c < table[currentStep].length; c++){
        checkAnswer(currentStep, c);
      }
      currentStep++;
    }
  };


//////////////////////////////
// Animation Stuff

  var timerID;
  var counter;

  //click a cell, then click the animate button
  function animate() {
    // $('.jsavcontrols').show();
    var i = 0;
    //this setInterval has to put function(){} to make it work
    timerID = setInterval(function() {animationHelper();}, 1000);
  };

  function animationHelper() {
    if(counter === undefined) {
      counter = 0;
    }
    if(counter >= oldrow){
      unhighlightPrevious();
      counter = 0;
      clearInterval(timerID);
    }else{
      //if previously highlighted other cells, unhighlight them
      if(counter >= 1){
        unhighlightPrevious();
      }
      jsavParseTable.highlight(counter, oldcol);
      jsavParseTable.highlight(oldrow-counter-1, oldcol+counter+1);
      counter++;
    }

    function unhighlightPrevious(){
      jsavParseTable.unhighlight(counter-1, oldcol);
      jsavParseTable.unhighlight(oldrow-counter, oldcol+counter);
    }
  };

///////////////////////////


  $('#inputbutton').click(enterInput);
  $('#completebutton').click(completeCYKTable);
  $('#stepbutton').click(step);
  $('#animatebutton').click(animate);

  $(document).click(defocus);



});