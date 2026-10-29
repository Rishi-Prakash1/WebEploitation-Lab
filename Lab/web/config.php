<?php
/* Database credentials. */
define('DB_SERVER', '127.0.0.1');   // TCP, not the Unix socket
define('DB_PORT',   3306);
define('DB_USERNAME', 'adrian');
define('DB_PASSWORD', 'P@sswr0d456');
define('DB_NAME', 'website');

/* Attempt to connect to MySQL database */
$mysqli = new mysqli(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_PORT);

/* new mysqli() never returns false - it returns an object with
   connect_errno set. Check that, not the object identity. */
if ($mysqli->connect_errno) {
    die("ERROR: Could not connect. " . $mysqli->connect_error);
}
?>
