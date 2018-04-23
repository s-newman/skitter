<?php
$ok = 0;

// Check image
$check = getimagesize($_FILES['upload']['tmp_name']);
if($check == false) {
    $ok++;
}

// Check file size
if($_FILES['upload']['size'] > 4000000) {
    $ok++;
}

// Generate URL
$hash = hex2bin(hash("sha256", $_FILES['upload']['tmp_name']));
$upload_url = "/img/".$hash.".png";

// Save image
if($ok === 0) {
    move_uploaded_file($_FILES['upload']['name'], $upload_url);
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
    mysqli_select_db($conn, "users");
    
    // Prepare statement
    $add_picture = $conn->prepare("INSERT INTO PROFILE_PICTURE (picture) VALUES (?)");
    $add_picture->bind_param("s", $upload_url);
    
    // Execute statement
    $add_picture->execute();
    $add_picture->close();

    $get_id = $conn->prepare("SELECT picture_id FROM PROFILE_PICTURE WHERE picture = ?");
    $get_id->bind_param("s", $upload_url);
    $get_id->execute();
    $get_id->bind_result($pic_id);
    $get_id->close();

    // Prepare statement
    $update_pic = $conn->prepare("UPDATE USER_INFO SET profile_picture_id = ? WHERE rit_username = ?");
    $update_pic->bind_param("ss", $pic_id, $_REQUEST['rit_username']);
    $update_pic->execute();
    
    // Close connections
    $update_pic->close();
    $conn->close();

    echo "File uploaded successfully.";
} else {
    echo "Failed to upload file.  There were ".$ok." errors.";
}
?>