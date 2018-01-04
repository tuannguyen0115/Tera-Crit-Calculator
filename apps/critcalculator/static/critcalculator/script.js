$(document).ready(function(){
    get_class_skills();
})
$(document).on("change", ".data",function(){
    get_crit();
})
$(document).on("keyup", ".data",function(){
    get_crit();
})
function get_class_skills(){    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        }               
    });                             
    $.ajax({
        url: '/get_class_skill',
        method: 'post',
        data: {
            class_id: $("#class-id").val()
        },
        success: function(serverResponse){
            $('#class-skil-generator').html(serverResponse)
        }
    }).done()          
}

function get_crit(){    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        }               
    });                             
    $.ajax({
        url: '/calculate_process',
        method: 'post',
        data: $("#ajax-form").serialize(),
        success: function(serverResponse){
            $('#ajax-form-crit-generate').html(
                "<p>Your crit chance is: </p>"+
                "<br>" +
                "<br>" +
                "<h1><b class='text-success'>"+ serverResponse + "%</b></h1>"
                )
        }
    }).done()              
}