$(document).ready(function () {
    setupAjaxDjango();

    $('.delete_attr').click(deleteAttribute);

    function deleteAttribute(evt) {
        var $target = $(evt.target).closest('button'),
            id = $target.data('id'),
            $attribute = $target.closest('.js-attributes__item');

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
                        toastr.success("Атрибут удален", "Успех!");
                    } else {
                        toastr.error(data["msg"]);
                    }
                },
                error: function (msg) {
                    toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
                }
            });
        } else {
            $attribute.remove();
        }
    }

    $('.delete_attr_value').click(deleteAttributeValue);

    function deleteAttributeValue(evt) {
        var $target = $(evt.target).closest('button'),
            id = $target.data('id'),
            $value = $target.closest('.attributes__item__value');
        if(id != '') {
            $.ajax({
                type: 'POST',
                url: $(this).data("href"),
                data: {
                    'id': id
                },
                success: function (data) {
                    if (data["code"] == 0) {
                        $value.remove();
                    } else {
                        toastr.error(data["msg"]);
                    }
                },
                error: function (msg) {
                    toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
                }
            });
        } else {
            $value.remove();
        }

    }

    $('.js-attributes__item__add-value').click(addAttributeValue);
	var self = this;
	function addAttributeValue (evt) {
		var $target = $(evt.target).closest('button'),
			$block = $('#attr_value_template').children().first(),
			$blockClone = $block.clone();

		$blockClone.find('.delete_attr_value').on('click', deleteAttributeValue);
		$blockClone.insertBefore($target);
		//// $block.find('.js-attributes__item__add-value').off('click', addAttribute);
		//$target.closest('button').remove();
    }

	$('.js-attributes__add-item').on('click', addAttribute);
	function addAttribute (evt) {
		var $target = $(evt.target),
			$block = $('.js-attributes__item-template').eq(0),
			$blockClone = $block.clone();
		$blockClone.removeClass('js-attributes__item-template').addClass('js-attributes__item');
		$blockClone.find('.js-attributes__item__add-value').on('click', addAttributeValue);
		//$blockClone.find('input').val('');
		$blockClone.find('.delete_attr').click(deleteAttribute);
		$blockClone.find('.delete_attr_value').click(deleteAttributeValue);
		$('.js-attributes').append($blockClone);
		$blockClone.removeClass('hide');
	}

	$('#add_attributes_form').on('submit', function(evt) {
		var submitData = [];
		var attrItems = $('.js-attributes__item');
		var attrs = [];
        $('button[type=submit]').addClass('disabled')
        _.each(attrItems, function(item) {
            var attrJSON = {
                id: $(item).find('input[name=id]').val(),
                name: $(item).find('input[name=name]').val(),
                values: []
            };

            _.each($(item).find('.attributes__item__value'), function(attributeValue){
                var attributeValueJSON = {
                    id: $(attributeValue).find('input[name=id]').val(),
                    value: $(attributeValue).find('input[name=value]').val()
                };
                attrJSON.values.push(attributeValueJSON);
            });
            //_.each($(item).find('input[name=value]'), function(attrValueInput) {
            //  attrJSON.values.push($(attrValueInput).val());
            //});
            attrs.push(attrJSON);
        });
        $('#add_attributes_form').find('input[name=form_data]').val(JSON.stringify(attrs));
        var formdata = new FormData($(this)[0]);
        $.ajax({
            type: 'POST',
            url: this.action,
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Данные обновлены', 'Успех!');
                    location.reload();
                }else{
                    toastr.error(data["msg"]);
                    $('button[type=submit]').removeClass('disabled')
                }
            },
            error: function(msg){
                $('button[type=submit]').removeClass('disabled');
                toastr.error('Что-то пошло не так, попоробуйте отправить заново', 'Ошибка!');
            }
        });


        return false;
	});

	// $('.js-objects__add-item').on('click', addObject);
	// function addObject (evt) {
	// 	var $target = $(evt.target),
	// 		$block = $('.js-objects__item').eq(0),
	// 		$blockClone = $block.clone();

	// 	$block.closest('.js-objects').append($blockClone);
	// }
});