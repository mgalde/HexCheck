// Note: This is a very basic check, more robust methods would involve AJAX, Fetch API, etc.

function checkServerStatus(callback) {
    // Using an image to check if PiHole web interface is up.
    var img = new Image();
    img.timeout = 5000; // 5 seconds timeout
    img.onload = function() {
        callback(true);
    };
    img.onerror = function() {
        callback(false);
    };
    img.src = "http://192.168.0.175/admin/img/favicon.png"; // A resource (like a favicon) from the PiHole web interface
}

function checkServiceStatus(serverIp, servicePort, callback) {
    // Using fetch or AJAX to check if a service is running can be a bit more involved 
    // due to potential CORS issues. Here's a basic method:
    fetch("http://" + serverIp + ":53" + servicePort)
    .then(response => {
        if (response.ok) callback(true);
        else callback(false);
    })
    .catch(error => {
        callback(false);
    });
}

// Example usage:
checkServerStatus(function(isOnline) {
    document.getElementById("server1-status").textContent = isOnline ? "Online" : "Offline";
    document.getElementById("server1-status").className = isOnline ? "online" : "offline";
    
    // Inferring DNS service status from web interface status:
    document.getElementById("server1-service").textContent = isOnline ? "Likely Running" : "Not Running";
    document.getElementById("server1-service").className = isOnline ? "online" : "offline";
});
    }
});

// Repeat for other servers...
