
$(function(){
	$( "#autofill" ).autocomplete({
    		source: '/search/',
    		minLength: 2,
    		autoFocus: true,
    		//delay: 200
  		});
});

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. 

function initAutocomplete() {

	// Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    var input2 = document.getElementById('input1');
    var searchBox2 = new google.maps.places.SearchBox(input2);
}


$(document).ready(function(){
	// tooltips
	$("#autofill").tooltip({
		position: {
                  my: "center bottom",
                  at: "center top-10",
                  collision: "none"
               }
	});
	$("#pac-input").tooltip({
		position: {
                  my: "center bottom",
                  at: "center top-10",
                  collision: "none"
               }
	});
	$("#input1").tooltip({
		 position: {
                  my: "center bottom",
                  at: "center top-10",
                  collision: "none"
               }
	});

	$(".form_container").css("margin-bottom", "133px");
	// click operation on div 
	$("#city").click(function(){
		$("#address").removeClass();
		$("#nearest").removeClass();
    	$("#city").addClass("active");
    	$("#placesSearch").hide();
    	$("#nearestSearch").hide();
    	$("#citySearch").show();
		$(".form_container").css("margin-bottom", "343px");
	});
	$("#address").click(function(){
		$("#city").removeClass();
		$("#nearest").removeClass();
    	$("#address").addClass("active");
    	$("#placesSearch").show();
    	$("#citySearch").hide();
    	$("#nearestSearch").hide();
		$(".form_container").css("margin-bottom", "343px");
	});
	$("#nearest").click(function(){
		$("#city").removeClass();
		$("#address").removeClass();
    	$("#nearest").addClass("active");
    	$("#nearestSearch").show();
    	$("#placesSearch").hide();
    	$("#citySearch").hide();
		$(".form_container").css("margin-bottom", "133px");
	});

	// default div
	$("#citySearch").hide();
	$("#placesSearch").hide();
	$("#nearest").addClass("active");

	// option button set
	$("#searchOption").buttonset();

	// operaion on toggleDiv on selecting radio button
	$("#toggleDiv").addClass("hidden");
	$("#searchOption").click(function(){
		//$("#closestAirport").val("");
		//$("#closestStation").val("");
		//$("#byWindows").prop('checked', false);
		//$("#byCustom").prop('checked', false);
    	if ($("#byWindows").is(':checked'))
    	{
      		$("#toggleDiv").addClass("hidden");
			$(".form_container").css("margin-bottom", "133px");
      		getLocation();
    	}
    	else
    	{
    		$("#toggleDiv").removeClass("hidden");
			$(".form_container").css("margin-bottom", "31px");
    	}
  	});

	$("#submitLocation").click(function(){
		$.ajax({
			type:'POST',
			url:'/customInput/',
			data:{
				addr:$("#input1").val(),
				csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
			},
			success:function(data){
				$("#closestAirport").val(data.airport);
				$("#closestStation").val(data.station);
				$("#closestCity").val(data.city);
			}
		});
	});

	// Mehod for retrieving location through web browser
	function getLocation() {
    	if (navigator.geolocation) {
        	navigator.geolocation.getCurrentPosition(showPosition, showError);
    	} 
    	else { 
        	$("#error").text("Geolocation is not supported by this browser.");
    	}
	}
	// callback function to get latitude and longitude
	function showPosition(position) {
		lat = position.coords.latitude;
    	lon = position.coords.longitude;
    	$.ajax({
			type:'POST',
			url:'/browser/',
			data:{
				lati:lat,
				longi:lon,
				csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
			},
			success:function(data){
				$("#closestAirport").val(data.airport);
				$("#closestStation").val(data.station);
				$("#closestCity").val(data.city);
			}
		});
	}
	// callback function to show error
	function showError(error) {
    	switch(error.code) {
        	case error.PERMISSION_DENIED:
            	$("#error").text("User denied the request for Geolocation.");
            	break;
        	case error.POSITION_UNAVAILABLE:
            	$("#error").text("Location information is unavailable.");
            	break;
        	case error.TIMEOUT:
            	$("#error").text("The request to get user location timed out.");
            	break;
        	case error.UNKNOWN_ERROR:
            	$("#error").text("An unknown error occurred.");
            	break;
    	}
	}


});



/*/simple ajax code to load data into a variable on focus event
$(document).ready(function(){
	$("#autofill").keyup(function(e){
		e.preventDefault();
		$.ajax({
			type:'POST',
			url:'/search/',
			data:{
				term:$( "#autofill" ).val(),
				csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
			},
			success:function(data){
				varb(data);
			}
		});
	});	
	function varb(data){
		//autocomplete using jquery-ui function autocomplete
		$( "#autofill" ).autocomplete({
    		source: data,
    		minLength: 2,
    		autoFocus: true,
    		delay: 200
  		});
	}

	// Overrides the default autocomplete filter function to search only from the beginning of the string
    /*$.ui.autocomplete.filter = function (array, term) {
        var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(term), "i");
        return $.grep(array, function (value) {
            return matcher.test(value.label || value.value || value);
        });
    };
});
*/