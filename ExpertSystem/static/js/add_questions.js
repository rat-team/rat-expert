$(document).ready(function () {
    setupAjaxDjango();


    //Удаляем вопрос
    var delete_question = $('.parameter__delete_question');
    delete_question.click(deleteQuestion);
    function deleteQuestion(event){
        var $target = $(event.target).closest('.btn');
        id = $target.data('id');
        $formgroup = $target.parent('.parameter__question_formgroup');
        if(id != '') {
            $.ajax({
                type: 'POST',
                url: $(this).data("href"),
                data: {
                    'id': id
                },
                success: function (data) {
                    if (data["code"] == 0) {
                        $formgroup.remove();
                    } else {
                        toastr.error(data["msg"]);
                    }
                },
                error: function (msg) {
                    toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
                }
            });
        } else {
            $formgroup.remove();
        }
    }


    //Добавление ответа
    var add_question = $('.parameter__add_question');
    add_question.click(addQuestion);
    function addQuestion(event){
        var $target = $(event.target).closest('.btn');
//        $questions_element = $target.parent('.parameter_questions_element');
        $block = $('.parameter__question_formgroup_template').eq(0);
        $block = $block.children().first();
        $blockClone = $block.clone();
        $blockClone.removeClass('parameter__question_formgroup_template').addClass('parameter__question_formgroup');
        $blockClone.find('.parameter__delete_question').on('click', deleteQuestion);
        $blockClone.insertBefore($target);
    }


    //Отправка вопросов
    var add_questions_form = $('#add_questions_form');
    add_questions_form.submit(function(){
        var parametersItems = $('.parameter_questions_element');
		var parametersQuestions = [];
        $('button[type=submit]').addClass('disabled');
		_.each(parametersItems, function(item) {
			var parameterJSON = {
				id: $(item).find('input[name=id]').val(),
				questions: []
			};

            var questions_formgroup = $(item).find('.parameter__question_formgroup');
            _.each(questions_formgroup, function(question_element){
                var type = $(question_element).find('select[name=type]').val();
                var question_id = $(question_element).find('input[name=question_id]').val();
                var q_body = $(question_element).find('textarea[name=body]').val();
                questionJSON = {
                    "type": type,
                    "id": question_id,
                    "body": q_body
                };

                parameterJSON.questions.push(questionJSON);
            });
			parametersQuestions.push(parameterJSON);
		});

        $('#add_questions_form').find('input[name=form_data]').val(JSON.stringify(parametersQuestions));
        var formdata = new FormData($(this)[0]);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Вопросы обновлены', 'Успех!');
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