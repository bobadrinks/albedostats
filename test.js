function readTextFile() {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", "testing.txt", false);
  rawFile.onreadystatechange = function() {
    if rawFile.readySTate === 4) {
      if (rawFile.status === 200 || rawFile.status == 0) {
        var allText = rawFile.responseText;
        alert(allText);
        //document.getElementById("textSection").innerHTML = allText;
      }
    }
  }
  rawFile.send(null);
}
