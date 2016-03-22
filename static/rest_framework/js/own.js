$(document).ready(function () {
    $("#user-answer").autocomplete({
        source: "/medicine-autocomplete/",
        minLength: 1,
    });
});

$(document).ready(function () {
    $("#history-list").autocomplete({
        source: "/history-search/",
        minLength: 1,
    });
});


$(document).ready(function () {

    $('#history-search').keyup(function () {

        $.ajax({
            type: "GET",
            url: "/history-search/",
            data: {
                'q': $('#history-search').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                $(".object-list").replaceWith(data)
            },
            dataType: 'html'
        });
    });
});


$(document).ready(function () {
    $('#answer-button').prop('disabled', true);
    $('#user-answer').prop('disabled', true);

    $('#user-answer').keyup(function () {
        if ($(this).val() != '') {
            $('button[type="submit"]').prop('disabled', false);
        }
    });
    $('input[type="radio"]').on('click', function () {
        if ($(this).parent().next()[0] != $(".ui-widget")[0]) {
            $('button[type="submit"]').prop('disabled', false);
            $('#user-answer').val('').prop('disabled', true);

        }
        else {
            $('#user-answer').prop('disabled', false);

            $('button[type="submit"]').prop('disabled', true);
        }
    });

});


$(document).ready(function () {
    $('#exchange-button').on('click', function (event) {
        event.preventDefault();
        Exchange();
    });
});

function Exchange() {
    var exchangeForm = $("#exchange-form");
    $.ajax({
        url: "/api/user/exchange/", // the endpoint
        type: "POST", // http method
        data: exchangeForm.serialize(), // data sent with the post request
        // handle a successful response
        success: function (json) {
            $('#score').html(json['score']);
            alert('Успешный обмен ' + json['exchange'] + ' баллов!');
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            alert('Что-то пошло не так... Попробуйте ещё раз или свяжитесь с администратором');
        }

    });
}

$(document).ready(function () {
    var but = $('#proceed-question');
    if (but.length) {
        but.prop('disabled', true);

        //var downloadButton = document.getElementById("download");
        var counter = 3;
        //var newElement = document.createElement("p");
        //newElement.innerHTML = "You can download the file in 10 seconds.";
        var id;

        //downloadButton.parentNode.replaceChild(newElement, downloadButton);

        id = setInterval(function () {
            counter--;
            if (counter < 0) {
                but.html("К опросу");
                but.prop('disabled', false);
                clearInterval(id);
            } else {
                but.html("Перейти к опросу через " + counter.toString() + " секунд");
            }
        }, 1000);
    }
});

//$(document).ready(function () {
    $('table').attr('width', '100%');
//});

