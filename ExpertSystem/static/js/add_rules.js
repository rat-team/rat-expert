$(document).ready(function () {
    setupAjaxDjango();

    var $rules = $('.js-rule[data-template=0]');
    _.each($rules, function(rule) {
        $(rule).find('.js-rule__condition:first-child').find('.js-rule__condition__remove-btn').remove();
        $(rule).find('.js-rule__result:first-child').find('.js-rule__result__remove-btn').remove();
    })

    //Добавляем правило параметр->параметр
    var add_parameter_rule = $('.rules__add_parameter_rule');
    add_parameter_rule.click(addParameterRule);
    function addParameterRule(event){
        $target = $(event.target).closest('.btn');
        $block = $('.rule_element_parameter_template').eq(0).children().first();
        $blockClone = $block.clone();

        $blockClone.find(".rule__delete_condition").click(deleteCondition);
        $blockClone.find(".rule__add_condition").click(addCondition);

        $blockClone.find(".rule__add_result").click(addResult);
        $blockClone.find(".rule__delete_result").click(deleteResult);

        $blockClone.find(".rule__delete").click(deleteRule);
        $blockClone.data("dddemplate", "1");

        $blockClone.attr('data-template', 0);

        $('.rules').append($blockClone);
    }
    //Параметр->атрибут
    var add_attribute_rule = $('.rules__add_attribute_rule');
    add_attribute_rule.click(addAttributeRule);
    function addAttributeRule(event){
        $target = $(event.target).closest('.btn');
        $block = $('.rule_element_attribute_template').eq(0).children().first();
        $blockClone = $block.clone();

        $blockClone.find(".rule__delete_condition").click(deleteCondition);
        $blockClone.find(".rule__add_condition").click(addCondition);

        $blockClone.find(".rule__add_result").click(addResult);
        $blockClone.find(".rule__delete_result").click(deleteResult);

        $blockClone.find(".rule__delete").click(deleteRule);
        $blockClone.attr('data-template', 0);

        $('.rules').append($blockClone);
    }


    //Добавляем condition
    var add_condition_btn = $('.rule__add_condition');
    add_condition_btn.click(addCondition);
    function addCondition(event){
        $target = $(event.target).closest('.btn');

        $conditionFormgroup = $target.parent('.condition_formgroup');
        $block = $('.rule_condition_template').eq(0).children().first();
        $blockClone = $block.clone();
        $blockClone.find(".rule__delete_condition").click(deleteCondition);
        $blockClone.find('.js-rule__condition__remove-btn').removeClass('hide');

        $blockClone.insertBefore($target);
    }


    //Удаляем условие
    var delete_condition_btn = $('.rule__delete_condition');
    delete_condition_btn.click(deleteCondition);
    function deleteCondition(event){
        $target = $(event.target).closest('.btn');
        $rule_condition_block = $target.closest('.rule_condition');
        $rule_condition_block.remove();
    }


    //Добавляем результат
    var add_result_btn = $('.rule__add_result');
    add_result_btn.click(addResult);
    function addResult(event){
        $target = $(event.target).closest('.btn');
        type = $target.data('type');
        if (type === 1){
            $block = $('.rule_result_attribute_template').eq(0).children().first();
        }else{
            $block = $('.rule_result_parameter_template').eq(0).children().first();
        }
        $blockClone = $block.clone();
        $blockClone.find(".rule__delete_result").click(deleteResult);

        $blockClone.find(".js-rule__result__remove-btn").removeClass('hide');

        $blockClone.insertBefore($target);
    }


    //Удаляем результат
    var delete_result_btn = $('.rule__delete_result');
    delete_result_btn.click(deleteResult);
    function deleteResult(event){
        $target = $(event.target).closest('.btn');
        $rule_result_block = $target.closest('.rule_result');
        $rule_result_block.remove();
    }


    //Удаляем правило
    var delete_rule_btn = $('.rule__delete');
    delete_rule_btn.click(deleteRule);
    function deleteRule(event){
        $target = $(event.target).closest('.btn');
        $rule_block = $target.closest('.rule_formgroup');
        $rule_block.remove();
    }

//ALI G INDAHOUSE
    $('form').on('submit', function(evt) {
        var $rules = $('.js-rule[data-template=0]'),
            rules = [];
        $('button[type=submit]').addClass('disabled');
        _.each($rules, function($rule) {
            var rule = {
                    condition: {
                        literals: [],
                        logic: []
                    },
                    result: [],
                    type: undefined
                },
                $conditions = $($rule).find('.js-rule__condition');
                $results = $($rule).find('.rule__result__select-block');

            //type
            rule.type = $($rule).find('input[name=type]').val();


            //condition
            _.each($conditions, function(condition) {
                var $condition = $(condition),
                    $logic = $condition.find('.js-rule__condition__literal-select_logic'),
                    literal = {};

                if ($logic.length) {
                    rule.condition.logic.push($logic.val())
                }

                literal.param = $condition.find('.js-rule__condition__literal-select_param1').val();
                literal.relation = $condition.find('.js-rule__condition__literal-select_relation').val();
                literal.value = $condition.find('.js-rule__condition__literal-select_param2').val();

                rule.condition.literals.push(literal);
                
            })

            //result
            _.each($results, function(result) {
                var $result = $(result);
                var resultObject = (rule.type == '0') ? 
                    {
                        'parameter': $result.find('.js-rule__result__select').val(),//id модели Parameter,
                        'values': $result.find('.js-rule__result__input').val()//текстовое значение параметра
                    }
                    : $result.find('.rule__result__select').val()
                rule.result.push(resultObject);
            })

            rules.push(rule);
        })
        $('form').find('input[name=form_data]').val(JSON.stringify(rules));

        var formdata = new FormData($(this)[0]);
        $.ajax({
            type: 'POST',
            url: this.action,
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data){
                if (data["code"] == 0) {
                    toastr.success('Правила обновлены', 'Успех!');
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