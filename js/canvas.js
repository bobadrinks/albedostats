/* 
 * Context Object wraps everything nicely; includes func to initialize
 * canvas.
 */
var Context = {
  canvas: null,
  context: null,
  create: function(canvas_tag_id) {
    this.canvas = document.getElementById(canvas_tag_id);
    this.context = this.canvas.getContext("2d");
    return this.context;
  }
};

// Main functionality here
$(document).ready(function() {

    /* "canvas" string - we get Element by ID from the html file */
    Context.create("canvas"); 

    function draw() {
      Context.context.beginPath();
      Context.context.fillStyle = "#ffffff";
      Context.context.fillRect(0,0,100,100);
      Context.context.closePath();
    }

    setInterval(daw, 10);

});
