$(document).ready(function () {
    setupAjaxDjango();

    $('.delete_answer').click(deleteAnswer);

    function deleteAnswer(evt) {
        var $target = $(evt.target).closest('button'),
            id = $target.data('id'),
            $answer = $target.closest('.form-group');

        alert('Удаление ответа ' + id );
        if(id != '') {
            $.ajax({
                type: 'POST',
                url: $(this).data("href"),
                data: {
                    'id': id
                },
                success: function (data) {
                    if (data["code"] == 0) {
                        $attribute.remove();
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
    //
	//$('#add_attributes_form').on('submit', function(evt) {
	//	var submitData = [];
	//	var attrItems = $('.js-attributes__item');
	//	var attrs = [];
	//	_.each(attrItems, function(item) {
	//		var attrJSON = {
	//			id: $(item).find('input[name=id]').val(),
	//			name: $(item).find('input[name=name]').val(),
	//			values: []
	//		};
    //
     //       _.each($(item).find('.attributes__item__value'), function(attributeValue){
     //           var attributeValueJSON = {
     //               id: $(attributeValue).find('input[name=id]').val(),
     //               value: $(attributeValue).find('input[name=value]').val()
     //           };
     //           attrJSON.values.push(attributeValueJSON);
     //       });
	//		//_.each($(item).find('input[name=value]'), function(attrValueInput) {
	//		//	attrJSON.values.push($(attrValueInput).val());
	//		//});
	//		attrs.push(attrJSON);
	//	});
	//	$('#add_attributes_form').find('input[name=form_data]').val(JSON.stringify(attrs));
     //   var formdata = new FormData($(this)[0]);
     //   $.ajax({
     //       type: 'POST',
     //       url: this.action,
     //       data: formdata,
     //       processData: false,
     //       contentType: false,
     //       success: function(data){
     //           if (data["code"] == 0) {
     //               toastr.success('Данные обновлены', 'Успех!');
     //           }else{
     //               toastr.error(data["msg"]);
     //           }
     //       },
     //       error: function(msg){
     //           toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
     //       }
     //   });
    //
     //   return false;
	//});

});