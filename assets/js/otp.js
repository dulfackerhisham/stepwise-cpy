// function timer(remaining) {
//   var m = Math.floor(remaining / 30);
//   var s = remaining % 30;
//   m = m < 10 ? "0" + m : m;
//   s = s < 10 ? "0" + s : s;
//   document.getElementById("countdown").innerHTML = `<small>Time left: ${m} : ${s}</small>`;
//   remaining -= 1;
//   if (remaining >= 0) {
//     setTimeout(function(){timer(remaining);}, 1000);
//     document.getElementById("resend").innerHTML = '&nbsp;';
//     return;
//   }
//   document.getElementById("resend").innerHTML = `<small class="d-none d-sm-block">Don't receive the OTP? &nbsp;</small> 
//   <small class="font-weight-bold text-decoration-underline fw-bold cursor" onclick="timer(60)">Resend OTP</small>`;
// }timer(30);

// const resend = document.getElementById('resend')
// resend.addEventListener("click", clickHandler)

// function clickHandler(e) {
//   e.preventDefault();

//   $.ajax({
//     method: 'GET', // Use GET method
//     url: '{% url "resend_otp" %}',
//     dataType: 'json', // Set dataType to 'json'
//     success: function(response) {
//       alert(response.message); // Show a success message (optional)
//       timer(30); 
//     }

//   })
// }

