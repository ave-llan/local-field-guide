var $cards = $('.speciesCard');
$cards.each(function(card) {
    var sciName = $(this).find('#scientific-name').text();
    $(this).find('#species-description').text(card);
    console.log(sciName);
})