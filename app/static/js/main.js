
function cancel_order(order_id){
    console.log(order_id)
    cancel_request(order_id)
}

function cancel_request(id) {
    $.ajax({
      url:"orders", //the page containing python script
      type: "PUT", //request type,
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(id),
      success:function(result){
        console.log(result);
      }
    });
  }
