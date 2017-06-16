<?php
    include("../reminder.php");
    if(isset($_POST["deleteKey"])) {
        
        $arr= array();
        if (($handle = fopen("../reminders.csv", "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
                array_push($arr,new Reminder($data[0],$data[1],$data[2],$data[3],$data[4],$data[5]));
            }
            fclose($handle);
        }
        usort($arr, "cmp");
        unset($arr[0]);

        file_put_contents("../reminders.csv", "");

        $fp = fopen('../reminders.csv', 'w');

        foreach ($arr as $singleRem) {
            fputcsv($fp, $singleRem->toArray());


        }
    echo "OKE";
    }
?>