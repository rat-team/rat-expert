$(document).ready(function () {
    setupAjaxDjango();

    var add_system_form = $('#add_system_form');
    add_system_form.submit(function(){
        var formdata = new FormData($(this)[0]);
        $('button[type=submit]').addClass('disabled');
        $.ajax({
            type: 'POST',
            url: '/insert_system/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Система добавлена', 'Успех!');
                    location.reload();
                }else{
                    $('button[type=submit]').removeClass('disabled')
                    toastr.error(data["msg"]);
                }
            },
            error: function(msg){
                $('button[type=submit]').removeClass('disabled')
                toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
            }
        });

        return false;
    })
});