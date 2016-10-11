var inputField = $('input[name="something"]');
$('.goUp').click(function() {
    inputField.val(inputField.val() + 1);
});

$('.goDown').click(function() {
    inputField.val(inputField.val() - 1);
});