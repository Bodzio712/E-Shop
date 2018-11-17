window.onload = function() {
//alert("section ok");


    window.onload = load_data();

    window.onload = test();

    function load_data() {
        get_products();
        get_category();
        get_manu();
        get_type();

    }

    function test() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_products",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var $div = $('#white_content')
            data = JSON.parse(response)
            for(i in data){
                alert(data[i][0])
            }

            alert(data);
        }
    })
//};
}

//PRZYKLADOWA FUNKCJA AJAX. POBIERA DANE Z FLASK URL I WYRZUCA DO <DIV WHITE_CONTENT>
function get_products() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_products",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            //alert(response);
            //var section = document.getElementById("white_content");
            //alert("section ok");
            //section.innerHTML = response;

        }
    })
//};
}

function get_category() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_categories",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            //alert(response);
            //var section = document.getElementById("white_content");
            //alert("section ok");
            //section.innerHTML = response;

        }
    })
//};
}

function get_manu() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_manufacturers",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            //alert(response);
            //var section = document.getElementById("white_content");
            //alert("section ok");
            //section.innerHTML = response;

        }
    })
//};
}

function get_type() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_types",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            //alert(response);
            //var section = document.getElementById("white_content");
            //alert("section ok");
            //section.innerHTML = response;

        }
    })
//};
}
function display_cart() {
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/display_cart",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            //alert(response);
            //var section = document.getElementById("white_content");
            //alert("section ok");
            //section.innerHTML = response;

        }
    })
//};
}

//powinno sie uruchamiac po zlozeniu zamowienia i wyslaniu ajaxem
//informacji do placeorder
//function delete_cart() {
//    $.ajax({
//        type: "DELETE",
//        url: "http://127.0.0.1:5000/delete_cart",
//        dataType: "json",
//        contentType:"application/json",
//        success: function(response) {
//            alert(response);
//            //var section = document.getElementById("white_content");
//            //alert("section ok");
//            //section.innerHTML = response;
//
//        }
//    })
////};
//}


//var ref = document.getElementById("add2cart");
//ref.onclick = add2cart();
//function add2cart() {
//    //var id = $(this).attr("productId??????");
//    $.ajax({
//        type: "POST",
//        url: "http://127.0.0.1:5000/add_to_cart",// + id.toString(),
//        dataType: "text",
//        contentType:"application/json",
//        success: function(response) {
//            alert(response);
//            alert("dodano produkt do kosza")
//
//        }
//    })
////};
//}
//function remove_cart() {
//    //var id = $(this).attr("cartId??????");
//    $.ajax({
//        type: "PUT",
//        url: "http://127.0.0.1:5000/remove_from_cart/",// + id.toString(),
//        dataType: "text",
//        success: function(response) {
//            alert("udalo sie usunac")
//        }
//    });
//}
}
//#######################################

// Remove Items From Cart
$('a.remove').click(function(){
  event.preventDefault();
  $( this ).parent().parent().parent().hide( 400 );

})

// Just for testing, show all items
  $('a.btn.continue').click(function(){
    $('li.items').show(400);
  })


/* Set values + misc */
var promoCode;
var promoPrice;
var fadeTime = 300;

/* Assign actions */
$('.quantity input').change(function() {
  updateQuantity(this);
});

$('.remove button').click(function() {
  removeItem(this);
});

$(document).ready(function() {
  updateSumItems();
});


/* Recalculate cart */
function recalculateCart(onlyTotal) {
  var subtotal = 0;

  /* Sum up row totals */
  $('.basket-product').each(function() {
    subtotal += parseFloat($(this).children('.subtotal').text());
  });

  /* Calculate totals */
  var total = subtotal;


  /*If switch for update only total, update only total display*/
  if (onlyTotal) {
    /* Update total display */
    $('.total-value').fadeOut(fadeTime, function() {
      $('#basket-total').html(total.toFixed(2));
      $('.total-value').fadeIn(fadeTime);
    });
  } else {
    /* Update summary display. */
    $('.final-value').fadeOut(fadeTime, function() {
      $('#basket-subtotal').html(subtotal.toFixed(2));
      $('#basket-total').html(total.toFixed(2));
      if (total == 0) {
        $('.checkout-cta').fadeOut(fadeTime);
      } else {
        $('.checkout-cta').fadeIn(fadeTime);
      }
      $('.final-value').fadeIn(fadeTime);
    });
  }
}

/* Update quantity */
function updateQuantity(quantityInput) {
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.price').text());
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow.children('.subtotal').each(function() {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toFixed(2));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });

  productRow.find('.item-quantity').text(quantity);
  updateSumItems();
}

function updateSumItems() {
  var sumItems = 0;
  $('.quantity input').each(function() {
    sumItems += parseInt($(this).val());
  });
  $('.total-items').text(sumItems);
}

/* Remove item from cart
function removeItem(removeButton) {
  /* Remove row from DOM and recalc cart total */
/*  var productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
    updateSumItems();
  });
}*/
