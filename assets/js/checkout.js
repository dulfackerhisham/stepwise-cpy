$(document).ready(function () {
    
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();
        console.log("function called")

        var fname = $("input[name='fname']").val();
        var lname = $("input[name='lname']").val();
        var phone = $("input[name='phone']").val();
        var email = $("input[name='email']").val();
        var address = $("input[name='address']").val();
        var country = $("select[name='country']").val();
        var city = $("input[name='city']").val();
        var state = $("input[name='state']").val();
        var pincode = $("input[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        
        if(fname == "" || lname == "" || phone == "" || email == "" || address == "" || city == "" || state == "" || pincode == "" )
        {
            swal("Alert!", "All fields are mandatory!", "error");
            return false;
        }
        else
        {
            $.ajax({
                type: "GET",
                url: "/place-order/proceed-to-pay/",
                success: function (response) {
                    console.log("1 called")
                    var options = {
                        "key": "rzp_test_lyedGmf18EiO4x", // Enter the Key ID generated from the Dashboard
                        "amount": response.subtotal * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        // "amount": 1 * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "StepWise", //your business name
                        "description": "Thank you for buying from us",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            alert(responseb.razorpay_payment_id);
                            data = {
                                "fname": fname,
                                "lname": lname,
                                "phone": phone,
                                "email": email,
                                "address": address,
                                "country": country,
                                "city": city,
                                "state": state,
                                "pincode": pincode,
                                "payment_mode": "Paid by Razorpay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token,

                            }
                            $.ajax({
                                type: "POST",
                                url: "/place-order/",
                                data: data,
                                success: function (responsec) {
                                    console.log("2 called")


                                    swal("Congratulations", "your order has been placed successfully", "success").then((value) => {
                                        window.location.href = '/place-order/payment-completed/'
                                    });
                                    
                                }
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                            "name": fname+ " "+lname, //your customer's name
                            "email": email, 
                            "contact": phone  //Provide the customer's phone number for better conversion rates 
                        },
                        // "notes": {
                        //     "address": "Razorpay Corporate Office"
                        // },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });

        }
    
        
    });
});