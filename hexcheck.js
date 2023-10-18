// Note: This is a very basic check, more robust methods would involve AJAX, Fetch API, etc.

function checkServerStatus(serverIp, callback) {
    var img = new Image();
    img.onload = function() {
        callback(true);
    };
    img.onerror = function() {
        callback(false);
    };

    // This assumes servers will respond to a ping or request.
    img.src = "http://192.168.0.175/admin/" + serverIp;
}

function checkServiceStatus(serverIp, servicePort, callback) {
    // Using fetch or AJAX to check if a service is running can be a bit more involved 
    // due to potential CORS issues. Here's a basic method:
    fetch("http://192.168.0.175" + serverIp + ":53" + servicePort)
    .then(response => {
        if (response.ok) callback(true);
        else callback(false);
    })
    .catch(error => {
        callback(false);
    });
}

// Example usage:
checkServerStatus("192.168.1.1", function(isOnline) {
    document.getElementById("server1-status").textContent = isOnline ? "Online" : "Offline";
    document.getElementById("server1-status").className = isOnline ? "online" : "offline";

    if (isOnline) {
        checkServiceStatus("192.168.1.1", "8080", function(isServiceRunning) {
            document.getElementById("server1-service").textContent = isServiceRunning ? "Running" : "Not Running";
            document.getElementById("server1-service").className = isServiceRunning ? "online" : "offline";
        });
    }
});

// Repeat for other servers...
