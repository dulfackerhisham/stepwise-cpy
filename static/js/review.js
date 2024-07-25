console.log('working fine');

const monthNames = ["jan", "feb", "mar", "april", "may", "june",
"july", "aug", "sept", "oct", "nov", "dec"
];

$("#commentform").submit(function (e) {
    e.preventDefault();

    let date = new Date();
    let time = date.getDay() + ", " + monthNames[date.getUTCMonth] + ", " + date.getFullYear()

    $.ajax({
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        data: $(this).serialize(),
        dataType: "json",
        success: function (response) {
            console.log("comment saved to db")

            if (response.bool == true){
                $("#review-response").html("Review Added Successfully.")
                $(".hide-form").hide()
                $(".add-review").hide()

                let _html = '<div class="review_list mt-3">'
                        _html += '<div class="review_item">'
                        _html += '<div class="media">'
                        _html += '<div class="d-flex">'
                        _html += '<img style="width: 120px;" src="https://img.freepik.com/premium-vector/gray-avatar-icon-vector-illustration_276184-163.jpg" alt="">'
                        _html += '</div>'
                        
                        _html += '<div class="media-body">'
                        _html += '<h4>'+ response.context.user +'</h4>'
                        _html += '<div>'
                        _html += '<span class="font-xs text-muted">' + time + '</span>'
                        _html += '</div>'
                        
                        for(let i = 1; i <= response.context.rating; i++ ){
                        _html += '<i class = "fas fa-star text-warning"></i>'

                        }

                        _html += '</div>'
                        _html += '</div>'
                        _html += '<p>'+ response.context.review +' </p>'

                        _html += '</div>'
                        _html += '</div>'
                        $(".rating_list").prepend(_html)

            }
        }
    });
});