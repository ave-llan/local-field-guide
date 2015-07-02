L.mapbox.accessToken = 'pk.eyJ1IjoiZGlzdHJpY3RpbnJvYWRzIiwiYSI6Ik5pX2NMd2MifQ.VAzyiIlIyhmMduGNEUeGHw';

// select all the maps
$maps = $( ".field-guide-map" )

// create each map and set its view to the correct position
$maps.each(function(index) {
    var mapName = 'map' + String(index);
    var lat = $maps[index].getAttribute("latitude")
    var lng = $maps[index].getAttribute("longitude")
    var map = L.mapbox.map(mapName, 'districtinroads.mjpi6m96', 
        { 
            zoomControl: false, 
            attributionControl: false
        });
    map.setView([lat, lng], 14)
})
