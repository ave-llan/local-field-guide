// For a specific field guide, fill each species card with photo from Flickr
// and a Wikipedia description


var $cards = $('.speciesCard');
$cards.each(function() {
    var card = $(this);
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
            // if key is -1, no article was found on wikipedia so do not add anything
            if (key != -1) {
                var url = 'http://en.wikipedia.org/wiki/' + data.query.pages[key].title;
                description.text(
                    data.query.pages[key].extract 
                    );
                description.append(' <a href="' + url + '" target="_blank">Wikipedia</a>');
            }
        }
    });

    var flickrUrl = 'https://api.flickr.com/services/rest/?' +
                    'method=flickr.photos.search&api_key=6417b277d897c7a6575bd941770bd1e5' +
                    '&sort=relevance&per_page=1&format=json&nojsoncallback=1' +
                    '&license=1,2,3,4,5,6,7,8,9,10' +
                    '&text=' + sciName;
    $.ajax({
        url: flickrUrl,
        dataType: 'json',
        success: function(data) {
            var photo = data.photos.photo[0];
            // url to the actual photo
            var photoUrl = 'https://farm' + photo.farm + 
                           '.staticflickr.com/' + photo.server +
                           '/' + photo.id + '_' + photo.secret +
                           '_z.jpg';
            // url to the photo on Flickr
            var photoPage = 'https://www.flickr.com/photos/' +
                            photo.owner + '/' + photo.id;
            card.prepend(
                '<figure>' +
                '<img src="' + photoUrl + '">' +
                '<figcaption><a href="' + photoPage + '" target="_blank">Image from Flickr</a></figcaption>' +
                '</figure>'
                );
        }
    })
})