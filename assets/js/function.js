$(document).ready(function() {

    $('.increment-btn').on("click" ,function (e){
        e.preventDefault();
        
        let maxStock = parseInt($(this).closest('.product_data').find('.max-stock').val(), 10);
        let currentQty = parseInt($(this).closest('.product_data').find('.qty').val(), 10);

        if (currentQty < maxStock) {
            currentQty++;
            $(this).closest('.product_data').find('.qty').val(currentQty);
        }else {
            alertify.error("Product only have " + maxStock + " Stocks Available" );
        }

        console.log(maxStock, "max stock")
        console.log(currentQty, "current qty")
    });

    $('.decrement-btn').on("click" ,function (e){
        e.preventDefault();
        console.log("its working")
    
        var dec_value = $(this).closest('.product_data').find('.qty').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1){  // Decrement only if value is greater than 1
            value--;
            $(this).closest('.product_data').find('.qty').val(value);  // Corrected selectors
        }
    });

    // Add to cart functionality
    // now we are taking the quantity input field value when we click on 'add to cart' button
    $(".add-to-cart-btn").on("click", function(e){
        e.preventDefault();

        console.log("function is called");
        let quantity = $("#sst").val()
        // let product_title = $(".product-title").val()
        let product_id = $(".product-id").val()
        // let product_price = $(".product-price").text()
        // let this_val = $(this)
        var token = $('input[name=csrfmiddlewaretoken]').val();

        console.log("quantity:", quantity);
        // console.log("product title:", product_title);
        console.log("product id:", product_id);
        // console.log("product price:", product_price);
        // console.log("Current Element:", this_val);

        $.ajax({
            type: "POST",
            url: "/cart/add_to_cart/",
            data: {
                'id': product_id,
                'qty': quantity,
                // 'title': product_title,
                // 'price': product_price,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            beforeSend: function() {
                console.log("Adding product to Cart");
            },
            success: function(response){
                console.log(response)
                alertify.success(response.status)
                // window.alert(response.status)
                console.log("Added product to Cart");
            }
        })
})

$('.changeQuantity').click(function (e){
    e.preventDefault();
    // let product_id = $(".product-id").val()

    var product_id = $(this).closest('.product_data').find('.product-id').val();
    var product_qty = $(this).closest('.product_data').find('.qty').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();
    
    console.log("called func");
    console.log(product_id, "product id");
    console.log(product_qty, "quantity");

    var totalPriceElement = $(this).closest('tr').find('.total-price'); // Find the specific .total-price element within the same table row
    var subtotalElement = $(this).closest('tr').find('.subtotal'); // Find the specific .subtotal element within the same table row



    $.ajax({
        type: 'POST',
        url : '/cart/update-cart/',
        data: {
            'id': product_id,
            'qty': product_qty,
            csrfmiddlewaretoken: token,
        },
        dataType: 'json',
        success: function (response) {
            if (response.status === "Updated Successfully") {
                // Update the displayed total price with the new total price
                var newTotalPrice = parseInt(response.new_total_price); // Format as a floating-point number with 2 decimal places
                totalPriceElement.text('Rs ' + newTotalPrice);

                // Update the displayed subtotal
                var newSubtotal = parseInt(response.subtotal); // Format as a floating-point number with 2 decimal places
                $('#subtotal').text('Rs ' + newSubtotal);

                // alertify.success(response.status);
            } else {
                alertify.error(response.status);
            }
        }
    })
})

    $(".add-to-wishlist").on("click", function(e){
        e.preventDefault();

        console.log("function is called");

        let product_id = $(".product-id").val()

        var token = $('input[name=csrfmiddlewaretoken]').val();

        console.log("product id:", product_id);


        $.ajax({
            type: "POST",
            url: '/wishlist/add_to_wishlist/',
            data: {
                'id': product_id,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            beforeSend: function() {
                console.log("Adding product to Wishlist");
            },
            success: function(response){
                console.log(response)
                alertify.success(response.status)
                // window.alert(response.status)
                console.log("Added product to Wishlist");
            }
        })
    })

    // Attach an event listener to the document to handle delete cart button clicks
$(document).on('click', '.delete-cart', function (e) {
    e.preventDefault();
        // let product_id = $(".product-id").val()

        var row = $(this).closest('tr'); // Get the parent row of the clicked delete button
        var product_id = row.find('.product-id').val(); // Find product ID within the row
        var product_qty = row.find('.qty').val(); // Find product quantity within the row
        var token = $('input[name=csrfmiddlewaretoken]').val();
        console.log("called func");
        console.log(product_id, "product id");
        console.log(product_qty, "quantity");

        $.ajax({
            type: 'POST',
            url : '/cart/delete-cart/',
            data: {
                'id': product_id,
                'qty': product_qty,
                csrfmiddlewaretoken: token,
            },
            dataType: 'json',
            success: function (response) {
                console.log("product deleted")
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata");

            }
        })
    })


    // Attach an event listener to the document to handle delete wishlist button clicks
    $(document).on('click', '.delete-wishlist', function (e) {
        e.preventDefault();

        var wishId = $(this).data('id'); // Get the wishlist item ID
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: '/wishlist/delete-wishlist/',
            data: {
                'id': wishId,
                csrfmiddlewaretoken: token,
            },
            dataType: 'json',
            success: function (response) {
                console.log("wishlist item deleted");
                alertify.success(response.status);

                // Reload the wishlist data after deletion
                $('.wishlist-container').load(location.href + " .wishlist-container", function () {
                    // Re-attach event listeners to the newly loaded content
                    // attachDeleteWishlistEventListeners();
                });
            }
        });
    });

    // Function to attach event listeners to delete wishlist buttons
    function attachDeleteWishlistEventListeners() {
        $('.delete-wishlist').off('click'); // Remove previous event listeners
        $('.delete-wishlist').on('click', function (e) {
            // Handle the delete wishlist item logic as before
        });
    }

    // Initial call to attach event listeners
    attachDeleteWishlistEventListeners();

    

    // Function to attach event listeners to delete buttons
    function attachDeleteEventListeners() {
        $('.delete-cart').off('click'); // Remove previous event listeners
        $('.delete-cart').on('click', function (e) {
            // Handle the delete logic as before
        });
    }

    // Initial call to attach event listeners
    attachDeleteEventListeners();


    // Making Default Address
    $(document).on("click", ".make-dafault-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID is", id);
        console.log("Element is:", this_val);

        $.ajax({
            url: "/login/make-default-address/",
            data: {
                "id":id,
            },
            dataType: "json",
            success: function(response){
                console.log("Address Make Default");
                if (response.boolean == true){

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()


                }
            }

        })
    })

    
});
