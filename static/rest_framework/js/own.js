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



$(document).ready(function() {

    $('#history-search').keyup(function() {

        $.ajax({
            type: "GET",
            url: "/history-search/",
            data: {
                'q' : $('#history-search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(data){
                $('ul').replaceWith(data)
            },
            dataType: 'html'
        });
    });
});




$(document).ready(function() {
     $('button[type="submit"]').prop('disabled', true);
     $('#user-answer').prop('disabled', true);

     $('#user-answer').keyup(function() {
        if($(this).val() != '') {
           $('button[type="submit"]').prop('disabled', false);
        }
     });
    $('input[type="radio"]').on('click', function () {
        if ($(this).parent().next()[0] != $(".ui-widget")[0]) {
            $('button[type="submit"]').prop('disabled', false);
             $('#user-answer').val('').prop('disabled', true);

        }
        else{
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