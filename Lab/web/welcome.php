<?php
// Initialize the session
session_start();

// Check if the user is logged in, if not then redirect him to login page
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: index.php");
    exit;
}

// Use the shared connection instead of a hardcoded 'localhost' one.
// config.php is patched by the Dockerfile to 127.0.0.1 (TCP); a local
// 'localhost' connection here would use the unusable Unix socket.
require_once "config.php";

$message = "";
if(isset($_POST['submit'])){ //check if form was submitted
  $input = $mysqli->real_escape_string($_POST['url']);
  $sql = "INSERT INTO links (link) VALUES ('$input')";
  if($mysqli->query($sql) === true){
    $message = "Thank you for your submission, you have entered: <a href='$input' target='_blank' >Here</a>";
  } else{
    // Surface the real reason instead of the placeholder text
    error_log("link insert failed: " . $mysqli->error);
    $message = "Thank you for your submission!";
  }
}else{
  $message = "It is totally free!";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body{ font: 14px sans-serif; text-align: center; }
    </style>
</head>
<body>
    <h1 class="my-5">Hello, <b><?php echo htmlspecialchars($_SESSION["username"]); ?></b>! Welcome to our free blog promotions site.</h1>
    <h1 class="my-5">Please submit your link so that we can get started. All links will be reviewed by our admin</h1>
    <form action="" method="post">
                <label for="link">Blog Link:</label>
                <input type="text" placeholder='http://visitme.com/' id="link" name="url"><br><br>
                <input type="submit" name="submit" value="Submit">
                <br>
                <br>
                <?php echo "<p>{$message}</p>"; ?>
    </form>
    <br>
    <p>
        <a href="reset-password.php" class="btn btn-warning">Reset Your Password</a>
        <a href="logout.php" class="btn btn-danger ml-3">Sign Out of Your Account</a>
    </p>

</body>
</html>
