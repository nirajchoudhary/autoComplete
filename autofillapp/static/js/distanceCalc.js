
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;
var d;
function initialize() {
	directionsDisplay = new google.maps.DirectionsRenderer();
}

function calcRoute(end) {
	var start = document.getElementById("start").value;
	//var end = document.getElementById("end").value;
	var distanceInput = document.getElementById("distance");
			
	var request = {
		origin:start, 
		destination:end,
		travelMode: google.maps.DirectionsTravelMode.DRIVING
	};
	
	directionsService.route(request, function(response, status) {
		if (status == google.maps.DirectionsStatus.OK) {
			directionsDisplay.setDirections(response);
			d = (response.routes[0].legs[0].distance.value) / 1000.0;
			distanceInput.value = d;
			//return false;
		}
	});
	//return d;
}

/*
<script>
var x = document.getElementById("demo");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    x.innerHTML = "Latitude: " + position.coords.latitude + 
    "<br>Longitude: " + position.coords.longitude;	
}
</script>
*/