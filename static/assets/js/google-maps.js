function initMap() {
    // Latitude and Longitude
    var myLatLng = {lat: 35.73625402058657 , lng: 10.575000374803404};

    var map = new google.maps.Map(document.getElementById('myMap'), {
        zoom: 17,
        center: myLatLng
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'South Jakarta, INA' // Title Location
    });
}