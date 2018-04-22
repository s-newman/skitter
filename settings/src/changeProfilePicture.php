<?php
// Prepare db connection
$host = "user-db";
$user = "api-gateway";
$pass = "changemeplease-securitysucks";

// Connect
$conn = new mysqli($host, $user, $pass);
while($conn->connect_error) {
    usleep(5000000);
    $conn = new mysqli($host, $user, $pass);
}

// 

// Close db connection
$conn->close();
?>