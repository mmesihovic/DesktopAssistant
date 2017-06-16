<?php 
session_start();

    if(isset($_SESSION["user"])) {
        header("Location: dashboard.php");
        die();
    }
if(isset($_POST["name"])) {
    if($_POST["pin"]==97531 && $_POST["name"]=="PiMan") {
        $_SESSION["user"] = $_POST["name"]; // Validacija!!!
        header("Location: dashboard.php");
        die();
    }
    else {
        header("Location: login.php?err=1");
        die();
    }
}
else {
    header("Location: login.php");
    die();
}


?>