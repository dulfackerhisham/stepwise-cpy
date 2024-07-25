$(document).ready(function (){
    $(".filter-box, #filertBtn").on("click" , function (){
        console.log("A checkbox has been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-box").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            // console.log("filter value is:", filter_value);
            // console.log("filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("filter object is: ", filter_object);
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending Data.....")
            },
            success: function(response){
                console.log(response);
                console.log("data filtered successfully")
                $("#filtered-product").html(response.data)

            }

        })
    })

    // Setting blur function for price range
    $("#filertBtn").on("click", function () {
        // console.log("Is this function working");

        let min_price = $("#max_price").attr("min");
        let max_price = $("#max_price").attr("max");
        let current_price = $("#max_price").val();

        console.log("Current Price is:", current_price);
        console.log("Max Price is:", max_price);
        console.log("Min Price:", min_price);

        // Check if user entered price is within the original price limits
        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            console.log("Price Error Occured");
            alert("Price must be between Rs"+ min_price + ' and Rs' + max_price)
            $("#max_price").val()
            $("#range").val(min_price)
            $("#max_price").focus()

            return false
        }
})


})



