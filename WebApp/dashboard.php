<?php
    require('reminder.php');
    session_start();
$user ="";
    if(!isset($_SESSION["user"])) {
        header("Location: login.php");
        die();
    }
    else {
        $user = $_SESSION["user"];
    }
    
    $arr= array();

    if (($handle = fopen("reminders.csv", "r")) !== FALSE) {
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            array_push($arr,new Reminder($data[0],$data[1],$data[2],$data[3],$data[4],$data[5]));
        }
        fclose($handle);
    }
    

?>
    <html>

    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="css/PiStyle.css">
        <title>Pip The French</title>
    </head>

    <body>
       <a href="logout.php" class="logout btn btn-default">Sign out</a>
        <div class="row valigned">
            <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4 col-lg-4 col-lg-offset-4">
                <h1 class="white-text">Hello <?php echo $user; ?></h1> 
                <h3 class="white-text">Reminders</h3>
                <div class="list-group">
                   <?php
                    if(sizeof($arr)==0) {
                        echo ("<a href=\"#\" class=\"list-group-item \">");
                        echo("<h4 class=\"list-group-item-heading\">If you need to be reminded of anything just press the '+' icon in the top left corner :) </h4>");
                        echo("</a>");
                    } 
                    else {
                        foreach($arr as $key=>$entry) {
                            echo ("<span ondblclick=\"promptDelete(".$key.")\" class=\"list-group-item \">");
                            echo("<h4 class=\"list-group-item-heading\" style=\"word-break:break-all;\">".$entry->reminder."</h4>");
                            echo("<p class=\"list-group-item-text\">".$entry->printDate()."</p>");
                            echo("</span>");
                        }
                    }
                    
                    
                    ?>
                    
                        
                        
                
                </div>
            </div>
        </div>
        <span class="glyphicon glyphicon-plus add btn btn-default" aria-hidden="true"  data-toggle="modal" data-target="#myModal"></span>
<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
 <div class="vertical-alignment-helper">
  <div class="modal-dialog vertical-align-center" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">Add new reminder</h4>
      </div>
    <form action="addReminder.php" method="post" class="form-horizontal">
      <div class="modal-body">
            <div class="form-group">
            <label for="inputMsg" class="col-sm-2 control-label">Reminder</label>
            <div class="col-sm-10">
                <input type="text" maxlength="50" class="form-control" id="inputMsg" name="inputMsg" placeholder="Reminder message"> </div>
            </div>
            <div class="form-group">
            <label for="inputYear" class="col-sm-2 control-label">Year</label>
            <div class="col-sm-10">
                <input type="number" class="form-control" id="inputYear" name="inputYear" placeholder="2017" min="2017" max="2100"> </div>
            </div>
            <div class="form-group">
            <label for="inputMonth" class="col-sm-2 control-label">Month</label>
            <div class="col-sm-10">
                <input type="number" class="form-control" id="inputMonth" name="inputMonth" placeholder="12" min="1" max="12"> </div>
            </div>
            <div class="form-group">
            <label for="inputDay" class="col-sm-2 control-label">Day</label>
            <div class="col-sm-10">
                <input type="number" class="form-control" id="inputDay" name="inputDay" placeholder="12" min="1" max="31"> </div>
            </div>
            <div class="form-group">
            <label for="inputHour" class="col-sm-2 control-label">Hour</label>
            <div class="col-sm-10">
                <input type="number" class="form-control" id="inputHour" name="inputHour" placeholder="22" min="0" max="23"> </div>
            </div>
            <div class="form-group">
            <label for="inputMinute" class="col-sm-2 control-label">Minute</label>
            <div class="col-sm-10">
                <input type="number" class="form-control" id="inputMinute" name="inputMinute" placeholder="15" min="0" max="59"> </div>
            </div>
            
            
        
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Abort</button>
        <input type="submit" class="btn btn-primary" value="Add" name="add">
      </div>
    </form>
    </div>
    </div></div>
</div>
<div class="projectInfo">Double click on a report to delete it
    </div>
   <script src="js/jquery-3.2.1.min.js"></script>
   <script src="bootstrap/js/bootstrap.min.js"></script>
   <script src="js/script.js"></script>
    </body>

    </html>