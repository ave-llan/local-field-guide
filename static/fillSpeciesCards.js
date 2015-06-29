var $cards = $('.speciesCard');
$cards.each(function(card) {
    var sciName = $(this).find('#scientific-name').text();
    var description = $(this).find('#species-description');

    // load wikipedia description
    var wikiUrl = 'https://en.wikipedia.org/w/api.php?' +
                  'format=json&action=query&prop=extracts&exintro=' + 
                  '&explaintext=&redirects=&exsectionformat=plain&exsentences=2' +
                  '&titles=' + sciName;
    $.ajax({
        url: wikiUrl,
        dataType: 'jsonp',
        success: function(data) {
            console.log(data);
            var key = Object.keys(data.query.pages)[0];
            var url = 'http://en.wikipedia.org/wiki/' + data.query.pages[key].title;
            description.text(
                data.query.pages[key].extract 
                );
            description.append(' <a href="' + url + '">Wikipedia</a>');
        }
    });
})