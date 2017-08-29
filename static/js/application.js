// Initialize "value" to be 0.75 (default global albedo value)
var value = 0.75;
// "readings" is where data gets appended, to be graphed
var readings = new TimeSeries();
// Add initial "default" values to the graph so it starts at 0.75
var endTime = Date.now();
for (var i = 0; i < 50; i++) {
  readings.append(new Date(endTime - i*500), 0.75);
}

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

// Main body of code
$(document).ready(function() {
    // Connect to the socket server.
    var socket = io('http://localhost');
    socket.on('connect', function() {
      socket.send("Hello, world");
      document.body.style.backgroundColor = '#cfc';
      });
    socket.on('disconnect', function() {
      document.body.style.backgroundColor = null;
      });
    socket.on('newnumber', function(msg) {
      console.log("Received number " + msg.number);
      document.getElementById('text').textContent = "no";
      value = parseFloat(msg.number);
      // On the canvas, update the TIME: __ ALBEDO: __ label with the albedo
      // value, rounded to 2 decimal places
      document.getElementById('text').textContent = 'TIME ' + (new Date()) 
      + ' ALBEDO: ' + (Math.round(value*100) / 100) + '\n';
      readings.append(new Date().getTime(), value);
      });
    // TODO: When code is working, remove this commented out code altogether
    /*
       var ws = new ReconnectingWebSocket('ws://localhost:8000/');
       ws.onopen = function() {
         document.body.style.backgroundColor = '#cfc';
       };
       ws.onclose = function() {
         document.body.style.backgroundColor = null;
       };
       ws.onmessage = function(event) {
         document.getElementById('text').textContent = "no";
         value = parseFloat(event.data);
         // On the canvas, update the TIME: __ ALBEDO: __ label with the albedo
         // value, rounded to 2 decimal places
         document.getElementById('text').textContent = 'TIME ' + (new Date()) 
           + ' ALBEDO: ' + (Math.round(value*100) / 100) + '\n';
         readings.append(new Date().getTime(), value);
       };
     */

/*
 * Create the actual chart and handle updating it;
 * This uses the smoothie-js library from Joe Walnes
 */
function createTimeline() {
  // Initialize the chart with some default settings
  var chart = new SmoothieChart({
    fps: 30, millisPerPixel: 20, 
    grid: { 
      millisPerLine: 1000, verticalSections: 4,
    }, 
    interpolation:'bezier',
    minValue:0.0,
    maxValue:1.0
  });
  // This is where the chart gets data
  // We'll "update" the chart by appending data to this TimeSeries
  chart.addTimeSeries(readings, { 
    strokeStyle: 'rgba(0, 255, 0, 0.6)',
    fillStyle: 'rgba(0, 0, 255, 0.2)',
    lineWidth: 3 });
  // This chart streams to the canvas "chart" declared in HTML code
  chart.streamTo(document.getElementById("chart"), 1000);

  /* "canvas" string - we get Element by ID from the html file */
  Context.create("canvas"); 

  var albedo = 0.75;
  var BAR_WIDTH = 450;
  var BAR_HEIGHT = 10;
  var RADIUS = 5;
  var textYPos = 20;
  var xPos = 50;
  var yPos = 60;
  var MAX = BAR_WIDTH;
  var MIN = 0;

  // loops
  function draw() {
    drawBackground();
    albedo = Math.round(value*100)/100;
    drawAlbedoGauge();
  }

  function drawBackground() {
    Context.context.beginPath();
    Context.context.fillStyle = "#ff8100";
    Context.context.fillRect(0,0,canvas.width,canvas.height);
    Context.context.closePath();
  }

  // Function to create and draw healthbar
  function drawAlbedoGauge() {

    /* Bar underneath is gray */
    Context.context.fillStyle = "#a0a0a0";
    roundRect(Context.context, xPos, yPos,
      BAR_WIDTH, BAR_HEIGHT, RADIUS, false, false);
    Context.context.fill();
    Context.context.closePath();

    /* White text and bar */
    Context.context.beginPath();
    Context.context.fillStyle = "#ffffff";
    roundRect(Context.context, xPos, yPos, albedo * BAR_WIDTH, BAR_HEIGHT,
      RADIUS, true, false);
    Context.context.fill();
    Context.context.font = "42px Palatino";
    Context.context.fillText("Global Albedo " + albedo, xPos, canvas.height / 2);
    Context.context.closePath();
  }

  /**
   * Draws a rounded rectangle using the current state of the canvas.
   * If you omit the last three params, it will draw a rectangle
   * outline with a 5 pixel border radius
   * @param {CanvasRenderingContext2D} ctx
   * @param {Number} x The top left x coordinate
   * @param {Number} y The top left y coordinate
   * @param {Number} width The width of the rectangle
   * @param {Number} height The height of the rectangle
   * @param {Number} [radius = 5] The corner radius; It can also be an object 
   *                 to specify different radii for corners
   * @param {Number} [radius.tl = 0] Top left
   * @param {Number} [radius.tr = 0] Top right
   * @param {Number} [radius.br = 0] Bottom right
   * @param {Number} [radius.bl = 0] Bottom left
   * @param {Boolean} [fill = false] Whether to fill the rectangle.
   * @param {Boolean} [stroke = true] Whether to stroke the rectangle.
   */
  function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    if (typeof stroke == 'undefined') {
      stroke = true;
    }
    if (typeof radius === 'undefined') {
      radius = 5;
    }
    if (typeof radius === 'number') {
      radius = {tl: radius, tr: radius, br: radius, bl: radius};
    } else {
      var defaultRadius = {tl: 0, tr: 0, br: 0, bl: 0};
      for (var side in defaultRadius) {
        radius[side] = radius[side] || defaultRadius[side];
      }
    }
    ctx.beginPath();
    ctx.moveTo(x + radius.tl, y);
    ctx.lineTo(x + width - radius.tr, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
    ctx.lineTo(x + width, y + height - radius.br);
    ctx.quadraticCurveTo(x + width, y + height, 
      x + width - radius.br, y + height);
    ctx.lineTo(x + radius.bl, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
    ctx.lineTo(x, y + radius.tl);
    ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    ctx.closePath();
    if (fill) {
      ctx.fill();
    }
    if (stroke) {
      ctx.stroke();
    }

  }

  /* Tells the draw() function to repeat */
  setInterval(draw, 300);

}
