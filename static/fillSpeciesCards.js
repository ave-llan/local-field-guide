
var $cards = $('.speciesCard');
$cards.each(function() {
    var card = $(this);
    console.log(card);
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
            var key = Object.keys(data.query.pages)[0];
            // if key is -1, no article was found on wikipedia
            if (key != -1) {
                var url = 'http://en.wikipedia.org/wiki/' + data.query.pages[key].title;
                description.text(
                    data.query.pages[key].extract 
                    );
                description.append(' <a href="' + url + '">Wikipedia</a>');
            }
        }
    });

    var flickrUrl = 'https://api.flickr.com/services/rest/?' +
                    'method=flickr.photos.search&api_key=6417b277d897c7a6575bd941770bd1e5' +
                    '&sort=relevance&per_page=1&format=json&nojsoncallback=1' +
                    '&text=' + sciName;
    console.log(flickrUrl);
    $.ajax({
        url: flickrUrl,
        dataType: 'json',
        success: function(data) {
            var photo = data.photos.photo[0];

            var photoUrl = 'https://farm' + photo.farm + 
                           '.staticflickr.com/' + photo.server +
                           '/' + photo.id + '_' + photo.secret +
                           '_z.jpg';
            console.log(photoUrl);
            card.prepend('<img src="' + photoUrl + '">');
        }
    })
})