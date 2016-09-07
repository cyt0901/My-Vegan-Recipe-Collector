
$(document).on('click', '#update', function(evt) {
    $(this).nextUntil('div').toggle();
});

$(document).on('click', '#edit', function(evt) {
    evt.preventDefault();
    if (this.innerHTML == 'Edit My Recipes') {
        $('.to-toggle').toggle();
        $('.edit-notes').show();
        $(this).html('Cancel');
    } else {
        $('.to-toggle').toggle();
        $('.edit-notes').hide();
        $('.note-section').hide();
        $('.current-notes').show();
        $('.save-notes').hide();
        $('#edit').html('Edit My Recipes');
    }
});

$(document).on('click', '#save-label', function(evt) {
    var newLabel = $(this).prev().val();
    
    $.data(this.previousElementSibling, "newLabel", newLabel);

    var box_id = $(this).prev().data().box;
    var label_name = $(this).prev().data().newLabel;
    var info = {
        "box_id": box_id,
        "recipe_id": -1,
        "delete": "N",
        "label_name": newLabel
    };

    console.log(info);

    $.post('/update_my_recipes', info, updateMyRecipes);

});

$(document).on('click', '.edit-notes', function(evt) {
    $(this).toggle();
    $(this).prev().hide();
    $(this).nextUntil('div').show();
});

$(document).on('click', '.save-notes', function(evt) {
    var newNotes = $(this).prev().val();

    $.data(this.previousElementSibling, "notes", newNotes);

    var rec_id = $(this).prev().data().recipe;
    var box_id = $(this).prev().data().box;
    var notes = $(this).prev().data().notes;
    var info = {
        "box_id": box_id,
        "recipe_id": rec_id,
        "delete": "N",
        "notes": notes
    };

    console.log(info);

    $.post('/update_my_recipes', info, updateMyRecipes);

});

$(document).on('mouseover', '.glyphicon-remove', function(evt) {
    $('.alert').css('color', 'red');
});

$(document).on('mouseout', '.glyphicon-remove', function(evt) {
    $('.alert').css('color', '#333');
});

function updateMyRecipes(results) {
    $.get('/preview.html', function(results) {
        $('#preview').html(results);
    });

    $('#edit').click();
}

$(document).on('click', '.glyphicon-remove', function(evt) {
    var rec_id = $(this).data().recipe;
    var box_id = $(this).data().box;
    var info = {
        "box_id": box_id,
        "recipe_id": rec_id,
        "delete": "Y"
    };

    $.post('/update_my_recipes', info, updateMyRecipes);
});
