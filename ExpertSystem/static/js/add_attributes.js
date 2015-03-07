$(document).ready(function () {
    setupAjaxDjango();

    $('.js-attributes__item__add-value').click(addAttributeValue);
	var self = this;
	function addAttributeValue (evt) {
		var $target = $(evt.target).closest('button'),
			$block = $('#attr_value_template').children().first(),
			$blockClone = $block.clone();

		//$blockClone.find('.js-attributes__item__add-value').on('click', addAttributeValue);
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
		$blockClone.find('input').val('');
		$('.js-attributes').append($blockClone);
		$blockClone.removeClass('hide');
	}

	$('#add_attributes_form').on('submit', function(evt) {
		var submitData = [];
		var attrItems = $('.js-attributes__item');
		var attrs = [];
		_.each(attrItems, function(item) {
			var attrJSON = {
				name: $(item).find('input[name=name]').val(),
				values: []
			};
			_.each($(item).find('input[name=value]'), function(attrValueInput) {
				attrJSON.values.push($(attrValueInput).val());
			});
			attrs.push(attrJSON);
		});
		$('#add_attributes_form').find('input[name=form_data]').val(JSON.stringify(attrs));
        var formdata = new FormData($(this)[0]);
        $.ajax({
            type: 'POST',
            url: '/insert_attributes/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Атрибуты обновлены', 'Успех!');
                }else{
                    toastr.error(data["msg"]);
                }
            },
            error: function(msg){
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