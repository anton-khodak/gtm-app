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
            alert('Успешная выплата ' + json['exchange'] + ' гривен!');
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
        var val = but.text();
        but.prop('disabled', true);
        var counter = 15;
        var id;
        id = setInterval(function () {
            counter--;
            if (counter < 0) {
                but.html(val);
                but.prop('disabled', false);
                clearInterval(id);
            } else {
                but.html("Перейти к опросу через " + counter.toString() + " секунд");
            }
        }, 1000);
    }
});

// ADMIN

$(document).ready(function(){
    $(document).on('change', '#id_poll_type', function () {
       if ($(this).val() == "simple"){
           $('.field-text_ru, .field-text_uk').hide();
       }
        else{
           $('.field-text_ru, .field-text_uk').show();
       }
    });
});

$(document).ready(function(){
    if ($('#id_poll_type').find(':selected').text() == "Простой") {
        $('.field-text_ru, .field-text_uk').hide();
    }
});


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