  var layout = {
    title: 'Albedo',
    titlefont: {
      family: 'Courier New, monospace',
      size: 27,
      color: '#7f7f7f'
    },
    xaxis: {
      title: 'Time',
      titlefont: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    },
    yaxis: {
      title: 'Albedo Value',
      titlefont: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    },
    autosize: false,
    width: 600,
    height: 500,
    margin: {
      l: 80,
      r: 80,
      b: 100,
      t: 100,
      pad: 8
    },
  };
  var arrayLength = 30
  var newArray = []

  for(var i = 0; i < arrayLength; i++) {
    var y = Math.random()
    newArray[i] = y
  }

  Plotly.plot('stream', [{
    y: newArray,
    mode: 'lines',
    line: {color: '#80CAF6'}
  }], layout);

  var cnt = 0;

  var interval = setInterval(function() {

    // Adding new value to Graph's data array
    var y = Math.random()
    newArray = newArray.concat(y)
    // Removing oldest value from Graph's data array
    newArray.splice(0, 1)

    var data_update = {
      y: [newArray]
    };

    Plotly.update('stream', data_update)

    if(cnt === 100) clearInterval(interval);
  }, 200);
