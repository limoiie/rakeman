$(document).ready(function(){
  // todo
  // code below is about sticky header, now is commented
  // since sticky-header conflicts with material-lite. so
  // we just find another way to implement the sticky
  // header. but the method we used now stick header
  // all the time, we should find other time to reuse this
  // code.
  /*
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
  */
  $(document).ready(function(){
    // process query when 'return' key was click down
    $('#query_input').keydown(function(e) {
      if (e.keyCode === 13) {
        var query_string = $("#query_input")[0].value;
        // query by return always has page num 0 since it
        // should be the first query
        // todo: encode query string
        var query_url = "/'" + query_string + "'/0/query";
        $(location).attr('href', query_url);
      }
    });
  });
})
