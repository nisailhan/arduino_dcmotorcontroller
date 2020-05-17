jQuery(function($){
  function sell(item, delay){
    setTimeout( function(){
      item.addClass('move');
    }, delay);
    setTimeout( function(){
      item.removeClass('move');
      //sell( item, 11000) //go arbitrary numbers!
    }, delay + 5200)
  }
  
  var items = [];
  $('.item').each( function(){
    items.push( $(this) )
  });
  for( var i = 0, j = items.length; i < j; i++){
    var timing = i * 1000;
    var theItem = items[i];
    sell( theItem, timing )
  }
 })
