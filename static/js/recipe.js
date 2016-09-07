$('.btn-primary').on('mouseover', function(evt) {
    $('.glyphicon-star').css('color', '#FF9374');
});

$('.btn-primary').on('mouseout', function(evt) {
    $('.glyphicon-star').css('color', '#FFCC00');
});

function replaceNumbers(results) {
    var newResults = JSON.parse(results);

    for (var i=0; i<newResults.length; i++) {
        var usAmount = newResults[i].us_amount;
        var metAmount = newResults[i].metric_amount;
        var ingredient = newResults[i].ingredient;
        var extlink = newResults[i].extlink;

        $('#us'+i).html(usAmount);
        $('#met'+i).html(metAmount);
        if (newResults[i].extlink) {
            $('#inglink'+i).html('<a href="' + extlink + '" target="_blank">' + ingredient + '</a>');
        } else {
            $('#inglink'+i).html(ingredient);
        }
    }
}

function convert(evt) {
    evt.preventDefault();
    var info = {
        "serving": $('#serving').val(),
        "recipe_id": $('#recipe_id').val()
    };
    $.get('/show_conversion.json', info, replaceNumbers);
}

$('#conversion').on('submit', convert);