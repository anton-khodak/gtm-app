/**
 * Created by Abc on 31.05.2016.
 */

// SEND EVERY TIME A USER COMES IN

$(document).ready(function(){
    $.ajax({
       type: "POST",
       url: "/api/user/duration/",
       data:{
           'duration':'00:00',
           'csrfmiddlewaretoken': $(".session>input[name=csrfmiddlewaretoken]").val(),
           'browser': 'True'
       }
   })
});