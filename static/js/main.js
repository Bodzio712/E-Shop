window.onload = function() {
//alert("section ok");


    window.onload = load_data();

    add_navbar(); //dodawanie navbara
    showProducts(); //Wyswitlanie produktów
    show_cart_droptables(); // Wyświetlanie mozliowosci płatności i dostaw
    showCartItems(); // Wyswirtlanie zawartości koszyka
    showOrders(); // Wyswietlanie zamówionych produktów

    function load_data() {
        get_products();
        get_category();
        get_manu();
        get_type();

    }

        function showOrders() {
        $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/display_orders",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var $ord = $('#orders');
            var id =0;
            for(i in data) {
                if(id != data[i].date) {
                    $ord.append('<div class="basket-product"></div>');
                    id = data[i].date;
                }
                //alert(data[i].productName);
                $ord.append('<div class="item">' +
                    '          <div class="product-details">' +
                    '            <p><strong>'+data[i].productName+' </strong></p>' +
                    '          </div>' +
                    '        </div>' +
                    '        <div class="price">'+data[i].valueGross+'</div>' +
                    '        <div class = "quantity"><p style="margin: 0 0 15px 15px"> '+data[i].quantity+'</p></div>' +
                    '<div class="delivery">'+data[i].deliveryType+'</div>')

            }
        }
    })
    }


    function showCartItems() {
        $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/display_cart",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var $bas = $('#basket');
            for(i in data) {
                $bas.append('      <div class="basket-product">' +
                    '        <div class="item">' +
                    '          <div class="product-details">\n' +
                    '            <h1><strong><span class="item-quantity">'+data[i].quantity+' x </span>'+ data[i].productName +'</strong></h1>' +
                    '            <p><strong>Navy, Size 18</strong></p>' +
                    '            <p>Product Code - 232321939</p>' +
                    '          </div>' +
                    '        </div>' +
                    '\n' +
                    '        <div class="price">'+data[i].priceGross.toFixed(2)+'</div>' +
                    '        <div class="quantity">' +
                    '          <input type="number" value="'+data[i].quantity +'" min="1" class="quantity-field" name="quant">' +
                    '        </div>' +
                    '        <div class="subtotal" name="sub">'+(data[i].quantity*data[i].priceGross).toFixed(2) +'</div>' +
                    '        <a class="remove" href="/removeCart?cartId='+data[i].cartId+'">' +
                    '          <button>Usuń</button>' +
                    '        </a>' +
                    '      </div>')
            }
        }
    })
    }

    function show_cart_droptables() {
        $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/delivery_details",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var select = document.getElementById("deliveryOptions");
            for(i in data) {
                var option = document.createElement("option");
                option.value = data[i].deliveryId;
                option.text = data[i].deliveryType;
                select.add(option, null);
            }
        }
    })
        $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/payment_details",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var select = document.getElementById("paymentOptions");
            for(i in data) {
                var option = document.createElement("option");
                option.value = data[i].paymentId;
                option.text = data[i].paymentType;
                select.add(option, null);
            }
        }
    })
    }

    function add_navbar() {
        $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_categories",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var $cat = $('#catDropdown');
            for(i in data) {
                obj=data[i].categoryId;
                category="category";
                $cat.append('<a onclick="showProducts(\'' + category + '\',' + obj + ')">' + data[i].name +'</a>')
            }
        }
    })

         $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_types",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var $type = $('#typeDropdown');
            for(i in data) {
                obj=data[i].typeId;
                category="type";
                $type.append('<a onclick="showProducts(\'' + category + '\',' + obj + ')">' + data[i].name +'</a>');
            }
        }
    })

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_manufacturers",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var $man = $('#manDropdown');
            for(i in data) {
                obj=data[i].manufacturerId;
                category="manufacturer";
                $man.append('<a onclick="showProducts(\'' + category + '\',' + obj + ')">' + data[i].name +'</a>');
            }
        }
    })

        var number=0;


    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/is_logged",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/item_number",
            dataType: "json",
            contentType:"application/json",
            success: function(res) {
                number = JSON.parse(res);

                var data = JSON.parse(response);
                var $log = $('#navbar');
                var isLogged = false
                for(i in data) {
                    var x = data[i];
                    if(x.length == 4) {
                        isLogged = true;
                    }
                }
                if(isLogged == false) {
                    $log.append('<div class="dropdown">' +
                        '<a class="dropbtn" href="/loginForm">Zaloguj</a>' +
                        '</div>');
                } else {
                    $log.append('        <div class="dropdown">' +
                        '            <button class="dropbtn">Profil' +
                        '                <i class="fa fa-caret-down"></i>' +
                        '            </button>' +
                        '            <div class="dropdown-content" id="myDropdown">' +
                        '                <a href="/account/orders">Zamowienia</a>' +
                        '                <a href="/logout">Wyloguj</a>' +
                        '            </div>' +
                        '        </div>' +
                        '' +
                        '        <!-- Koszyk-->' +
                        '        <div id="cartId">' +
                        '<a class="link" href="/cart">' +
                        '<button class="cartClass">' +
                        '    <img src="/static/photos/cart.png" id="cartIcon" />' +
                        '                <p style="color: white">'+number+'</p>' +
                        '</button>' +
                        '\</a>' +
                        '</div>')
                }
            }
            })
        }
    })


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
  var x = document.getElementsByName('quant').values();
  setTimeout(function(){
      for(var item of x) {
      sumItems += parseInt(item.value);
  }
    $('.total-items').text(sumItems);
  }, 300);

  var sumVal = 0;
  var y = document.getElementsByName('sub');
  setTimeout(function(){
      for(var item of y) {
      sumVal += parseInt(item.innerText);
  }
    $('.subtotal-value').text(sumVal.toFixed(2));
      $('.total-value').text(sumVal.toFixed(2));
  }, 300);

}

function showProducts(attribute="", number=0){
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/load_products",
        dataType: "json",
        contentType:"application/json",
        success: function(response) {
            var data = JSON.parse(response);
            var toShowData = [];
            for(i in data) {
                if (attribute == "") {
                    toShowData = data;
                } else if (attribute == "category") {
                    if(data[i].categoryId == number) {
                        toShowData.push(data[i]);
                    }
                } else if (attribute == "type") {
                    if(data[i].typeId == number) {
                        toShowData.push(data[i]);
                    }

                } else if (attribute == "manufacturer") {
                    if(data[i].manufacturerId == number) {
                        toShowData.push(data[i]);
                    }
                }
            }
            makeProductsTable(toShowData);
            }
        })
}

function makeProductsTable(data) {
    $table = $('#products');
    $table.html('');
            for(i in data) {
                $table.append('<div class="basket-product">' +
                    '        <div class="item">' +
                    '          <div class="product-details">' +
                    '            <h1><strong><span class="item-quantity"> </span>' + data[i].description +'</strong></h1>' +
                    '            <p><strong>' + data[i].productName + '</strong></p>' +
                    '          </div>' +
                    '        </div>' +
                    '        <div class="price">' + data[i].priceGross+'</div>' +
                    '' +
                    '' +
                    '        <div class = "quantity" rel="modal:open">' +
                    '            <a href="#ex1" rel="modal:open" class="button">Szczegóły</a>' +
                    '            <div id="ex1" class="modal">' +
                    '                <p>' + data[i].description+'</p>' +
                    '            </div>' +
                    '        </div>' +
                    '' +
                    '        <div class="producent">'+data[i].name+'</div>' +
                    '' +
                    '        <div class = "quantity">' +
                    '              <form action="/addToCart?productId=' + data[i].productId +'" method="post" href="/addToCart?productId=' + data[i].productId+'">' +
                    '                       <td><input type = "number" name = "liczba" min = "0" maxlength="2" size="2"/></td>' +
                    '                       <input type = "hidden"  value =' + data[i].productId+' />' +
                    '                  <div class = "remove">' +
                    '                       <td><input type="submit" value="Dodaj do koszyka" id="add2cart"/></td>' +
                    '                  </div>' +
                    '              </form>' +
                    '        </div>' +
                    '' +
                    '' +
                    '' +
                    '</div>')

            }
            $table.append('</div>');
            $table.append('</div>');
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
