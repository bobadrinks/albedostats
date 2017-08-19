var fs = require('fs');
var path = "testing.txt";
var file = fs.readFileSync(path, "utf8");
var fileContent = file.toString();
fileContent = fileContent.replace(/(\r\n|\n\r)/gm,"");
fileContent = fileContent.trim();
console.log(fileContent);
var albedo = parseFloat(fileContent, 10);
console.log(albedo);
