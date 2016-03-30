// script for controling back and forward button of browser

window.onload = function () {
   	if (typeof history.pushState === "function") {
       	history.pushState("niraj", null, null);
       	window.onpopstate = function () {				// Handle the back (or forward) buttons here
           	history.pushState('nirajc', null, null);    // Will NOT handle refresh, use onbeforeunload for this.
    	};
   	}
   	else {
       	var ignoreHashChange = true;
       	window.onhashchange = function () {
	        if (!ignoreHashChange) {					// Detect and redirect change here
	            ignoreHashChange = true;				// it does mess with hash symbol (anchor?) pound sign
	            window.location.hash = Math.random();	// delimiter on the end of the URL
	        }
	        else {
	            ignoreHashChange = false;   
	  	    }
      	};
   	}
}

