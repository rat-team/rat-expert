$(document).ready(function () {
    setupAjaxDjango();

    //Удаляем AttributeValue
    var delete_attribute_value_btn = $('.delete_select_object_attribute_value');
    delete_attribute_value_btn.click(deleteAttributeValue);
    function deleteAttributeValue(event){
        var $target = $(event.target).closest('.btn');
        var formgroup = $target.parent('.attribute_value_formgroup');
        formgroup.remove();
    }


    //Добавляем селектор
    var add_attribute_value_btn = $('.object__add_attribute_value');
    add_attribute_value_btn.click(addAttributeValue);
    function addAttributeValue(event){
        $block = $('.object__attribute_value_template').eq(0);
        $block = $block.children().first();
        $blockClone = $block.clone();
        $blockClone.find('.delete_select_object_attribute_value').on('click', deleteAttributeValue);
        var $target = $(event.target).closest('.btn');
        $blockClone.insertBefore($target);
    }


    //Удаляем объект
    var delete_object_btn = $('.delete_object');
    delete_object_btn.click(deleteObject);
    function deleteObject(event){
        var $target = $(event.target).closest('.btn');
        $target.closest('.system_object').remove();
    }


    //Добавляем новый объект
    var add_new_object_btn = $('.add_new_object');
    add_new_object_btn.click(addNewObject);
    function addNewObject(event){
        objects = $('.objects');
        $block = $('.object_template').eq(0).children().first();
        $blockClone = $block.clone();
        $blockClone.removeClass('system_object_template').addClass('system_object');
        $blockClone.find('.delete_object').click(deleteObject);
        $blockClone.find('.object__add_attribute_value').click(addAttributeValue);
        $blockClone.find('.delete_select_object_attribute_value').click(deleteAttributeValue);

        objects.append($blockClone);
    }


    //Делаем снимок и инсертим в базу
    var add_objects_form = $('#add_objects_form');
    add_objects_form.submit(function(){
        var objectItems = $('.system_object');
		var objects = [];
        $('button[type=submit]').addClass('disabled');
		_.each(objectItems, function(item) {
			var objectJSON = {
				id: $(item).find('input[name=id]').val(),
				name: $(item).find('input[name=name]').val(),
				attribute_values: []
			};

            var object_attributes_values = $(item).find('.select__object_new_attribute_value');
            _.each(object_attributes_values, function(attributeValue){
                var id = $(attributeValue).find('select[name=object__attribute_value]').val();
                objectJSON.attribute_values.push(id);
            });
			//_.each($(item).find('input[name=value]'), function(attrValueInput) {
			//	attrJSON.values.push($(attrValueInput).val());
			//});
			objects.push(objectJSON);
		});

        $('#add_objects_form').find('input[name=form_data]').val(JSON.stringify(objects));
        var formdata = new FormData($(this)[0]);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Объекты обновлены', 'Успех!');
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