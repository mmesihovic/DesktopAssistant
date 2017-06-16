<?php
session_start();
    if(isset($_SESSION["user"])) {
        header("Location: dashboard.php");
        die();
    }
?>
<!DOCTYPE html>
<html lang="">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="css/PiStyle.css">
    <title>Pip The French</title>
</head>

<body class="" style="">
  <a href="https://github.com/Mustajbasic/deskassistant" class="githubLogo">
   <img src="github.png"  alt="Github">
  </a>
    <div class="row valigned">
       
        <div class="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4 col-lg-4 col-lg-offset-4">
           <h1 class="white-text">Login to Desk Assistant</h1>
           <?php 
                if(isset($_GET["err"])) {
            ?>
            <ul class="list-group">
                <li class="list-group-item red-text">Invalid user information</li>
                </ul>
            <?php }?>
            <form action="validate.php" method="post" class="" autocomplete="new-password">
               <input style="display:none" type="text" name="fakeusernameremembered"/>
                <input style="display:none" type="password" name="fakepasswordremembered"/>
                <div class="form-group">
                    <label for="inputName" class="white-text">Enter your name</label>
                    <input type="text" class="form-control" id="inputName" name="name" placeholder="Your Name">
                </div>
                
                <div class="form-group">
                    <label for="pin" class="white-text">Enter device access PIN</label>
                    <input type="password" class="form-control" id="pin" name="pin" placeholder="000000">
                </div>
                <input type="submit" class="btn btn-primary btn-block" value="Let me in">
            </form>
        </div>
    </div>
    
    <div class="projectInfo">Projekat za predmet 'Ugradbeni Sistemi' na Elektrotehničkom fakultetu u Sarajevu<br>
    Studenti: Mustajbašić Belmin(16796) i Mesihović Mirza(17345)<br>
    Profesor: Konjicija Samim<br>
    Asistentica: Zubača Jasmina
    </div>
</body>

</html>
<script src="js/jquery-3.2.1.min.js"></script>
<script src="bootstrap/js/bootstrap.min.js"></script>
<script src="js/script.js"></script>