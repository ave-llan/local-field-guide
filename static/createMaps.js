// Provide your access token
L.mapbox.accessToken = 'pk.eyJ1IjoiZGlzdHJpY3RpbnJvYWRzIiwiYSI6Ik5pX2NMd2MifQ.VAzyiIlIyhmMduGNEUeGHw';


$maps = $( ".field-guide-map" )

$maps.each(function(index) {
    var mapName = 'map' + String(index);
    console.log(mapName);
    L.mapbox.map(mapName, 'districtinroads.mjpi6m96');
})



