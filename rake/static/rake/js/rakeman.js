$(document).ready(function(){
  var ele = $('.sticky-row')
  ele.stickMe();
  ele.on('sticky-begin', function() {
    console.log("Began");
  })
  ele.on('sticking', function() {
    console.log("Sticking");
  })
  ele.on('top-reached', function() {
    console.log("Top reached");
  })
  ele.on('bottom-reached', function() {
    console.log("Bottom reached");
  })
})
