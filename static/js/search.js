
$('.expand-types').on('click', function(evt) {
    $('.expand-ingredients').toggle();
    $('.ingredient-type').toggle();
    $('.ingredient-name').hide();
    $('.expand-ingredients').html('Expand All Ingredients');
});

$('.expand-names').on('click', function(evt) {
    $(this).find('div').toggle();
    $('.expand-ingredients').html('Collapse All Ingredients');
});

$('.expand-ingredients').on('click', function(evt) {
    if ($(this).html() == 'Expand All Ingredients') {
        $(this).html('Collapse All Ingredients');
        $('.ingredient-name').show();
    } else {
        $(this).html('Expand All Ingredients');
        $('.ingredient-name').hide();
    }
});

$('.expand-courses').on('click', function(evt) {
    $('.course-name').toggle();
});