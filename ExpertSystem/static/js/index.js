
var deleteSystem = $('.delete-system');

var optionsRemoveSystem = {
    'title': "Удалить систему?",
    'singletone': true,
    'popout': true,
    'btnOkLabel': "Да",
    'btnCancelLabel': "Нет"
};
deleteSystem.confirmation(optionsRemoveSystem);

deleteSystem.on('click', function(){
    var system_id = $(this).data('id');
    $.get('/delete_system/' + system_id, function() {})
        .done(function(data) {
            if ('OK' in data) {
                $("#system" + system_id).remove();
                toastr.success('Система удалена', 'Успех!');
            }
            else {
                toastr.success('Не удалось удалить систему', 'Потрачено!');
            }
        })
        .fail(function(data) {
            toastr.success('Что-то пошло не так', 'Entschuldigung!');
        })
});