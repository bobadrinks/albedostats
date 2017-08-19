$(function(){
  var dynamic_data = JSON.parse(test.attr('data-dynamic'));

  $("div").data("role") === "page";
  $("div").data("lastValue") === 43;
  $("div").data("hidden") === true;
  $("div").data("options").name === "John";
});
