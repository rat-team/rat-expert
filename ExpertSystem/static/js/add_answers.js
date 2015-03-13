$(document).ready(function () {
    setupAjaxDjango();

    $('.delete_answer').click(deleteAnswer);

    function deleteAnswer(evt) {
        var $target = $(evt.target).closest('button'),
            id = $target.data('id'),
            $answer = $target.closest('.answer');
        if(id != '') {
            $.ajax({
                type: 'POST',
                url: '/delete_answer/',
                data: {
                    'id': id
                },
                success: function (data) {
                    if (data["code"] == 0) {
                        $answer.remove();
                    } else {
                        toastr.error(data["msg"]);
                    }
                },
                error: function (msg) {
                    toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
                }
            });
        } else {
            $answer.remove();
        }
    }

    $('.add_answer').click(addAnswer);
	var self = this;
	function addAnswer (evt) {
		var $target = $(evt.target).closest('button'),
			$block = $('#answer_template').children().first(),
			$blockClone = $block.clone();

		$blockClone.find('.delete_answer').on('click', deleteAnswer);
		$blockClone.insertBefore($target);
    }

	$('#add_answers_form').on('submit', function(evt) {
		var submitData = [];
		var questionItems = $('.question');
		var questions = [];
        $('button[type=submit]').addClass('disabled')
		_.each(questionItems, function(item) {
			var questionJSON = {
				id: $(item).find('input[name=id]').val(),
				answers: []
			};

            _.each($(item).find('.answer'), function(answer){
                var answerJSON = {
                    id: $(answer).find('input[name=id]').val(),
                    body: $(answer).find('input[name=body]').val(),
                    parameter_value: $(answer).find('input[name=parameter_value]').val()
                };
                questionJSON.answers.push(answerJSON);
            });
			questions.push(questionJSON);
		});
		$('#add_answer_form').find('input[name=form_data]').val(JSON.stringify(questions));
        var formdata = new FormData($(this)[0]);
        $.ajax({
            type: 'POST',
            url: this.action,
            data: { 'form_data': JSON.stringify(questions)},
            //processData: false,
            //contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Данные обновлены', 'Успех!');
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
	});

});