<?php
    session_start();
    
if(isset($_SESSION["user"])) {
    header("Location: dashboard.php");
    die();
}
else {
    header("Location: login.php");
    die();
}

?>