<?php
session_start();
    if(!isset($_SESSION["user"])) {
        header("Location: login.php");
        die();
    }

    if(!isset($_POST["add"])) {
        header("Location: dashboard.php");
        die();
    }
    else {
        include "reminder.php";
        
        $rem = new Reminder($_POST["inputYear"],
                           $_POST["inputMonth"],
                           $_POST["inputDay"],
                           $_POST["inputHour"],
                           $_POST["inputMinute"],
                           $_POST["inputMsg"]);
        $arr= array();

        if (($handle = fopen("reminders.csv", "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
                array_push($arr,new Reminder($data[0],$data[1],$data[2],$data[3],$data[4],$data[5]));
            }
            fclose($handle);
        }
        array_push($arr,$rem);
        usort($arr, "cmp");

        $fp = fopen('reminders.csv', 'w');
        
        foreach ($arr as $singleRem) {
            fputcsv($fp, $singleRem->toArray());
            
        }
        header("Location: dashboard.php");
        die();
    }
?>