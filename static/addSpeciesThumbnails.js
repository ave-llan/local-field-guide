// Select all divs which need a photo added on the main page
var $allSpecies = $('.species-thumbnail-preview');

// for each div, lookup the scientific name and find a photo from Flickr
$allSpecies.each(function() {
    var species = $(this);
    var sciName = $(this).attr("scientific-name");

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
            var photoUrl = 'https://farm' + photo.farm + 
                           '.staticflickr.com/' + photo.server +
                           '/' + photo.id + '_' + photo.secret +
                           '_q.jpg';
            var photoPage = 'https://www.flickr.com/photos/' +
                            photo.owner + '/' + photo.id;
            species.prepend('<img src="' + photoUrl + '">');
        }
    });
});