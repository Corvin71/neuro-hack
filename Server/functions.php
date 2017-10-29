<?php

function displayErrors($messages) {
    print("<b>Возникли следующие ошибки:</b>\n<ul>\n");

    foreach($messages as $msg){
        print("<li>$msg</li>\n");
    }
    print("</ul>\n");
}

function checkLoggedIn($status){
    switch($status){
        case "yes":
            if(!isset($_SESSION["loggedIn"])){
                header("Location: login.php");
                exit;
            }
            break;
        case "no":
            if(isset($_SESSION["loggedIn"]) && $_SESSION["loggedIn"] === true ){
                header("Location: members.php");
            }
            break;
    }
    return true;
}

function cleanMemberSession($login, $password) {
    $_SESSION["login"]=$login;
    $_SESSION["password"]=$password;
    $_SESSION["loggedIn"]=true;
}


function sql($query) {
    if (isset($_SESSION['login']) && isset($_SESSION['password'])) {
        $log=$_SESSION['login'];
        $pwd=$_SESSION['password'];

        $dbconn = @pg_connect("host=$host dbname=$dbname port=$port user=$log password=$pwd");
        if(!$dbconn)
        {
            $dbconn = @pg_connect("host=$host dbname=$dbname port=$port user=$dbname@$log password=$pwd");
            if(!$dbconn)
            {
                unset($_SESSION['login']);
                unset($_SESSION['password']);
                throw new Exception("Could not connect to database for user $log");
            }
        }

        $result = pg_query($dbconn, 'SET bytea_output = "escape"');
        if(!$result)
        {
            throw new Exception(pg_last_error());
        }

        $result = pg_query($dbconn, $query);
        if(!$result)
        {
            $error = pg_last_error();
            $pattern = "|ERROR: (.+?)CONTEXT|is";
            preg_match($pattern, $error, $out);
            throw new Exception($out[1]);
        }

        $response = array();
        while($line = pg_fetch_array($result, null, PGSQL_ASSOC))
        {
            $response[] = array_map('preprocess_data', $line);
        }
        pg_free_result($result);
        pg_close($dbconn);

        return $response;
    }
}



function sql_user($host, $dbname, $port, $login, $password, $query) {
        $log = $login;
        $pwd = $password;

        $dbconn = @pg_connect("host=$host dbname=$dbname port=$port user=$log password=$pwd");
        if(!$dbconn)
        {
            $dbconn = @pg_connect("host=$host dbname=$dbname port=$port user=$dbname@$log password=$pwd");
            if(!$dbconn)
            {
                throw new Exception("Could not connect to database for user $log");
            }
        }

        $result = pg_query($dbconn, 'SET bytea_output = "escape"');
        if(!$result)
        {
            throw new Exception(pg_last_error());
        }

        $result = pg_query($dbconn, $query);
        if(!$result)
        {
            $error = pg_last_error();
            $pattern = "|ERROR: (.+?)CONTEXT|is";
            preg_match($pattern, $error, $out);
            throw new Exception($out[1]);
        }

        $response = array();
        while($line = pg_fetch_array($result, null, PGSQL_ASSOC))
        {
            $response[] = array_map('preprocess_data', $line);
        }
        pg_free_result($result);
        pg_close($dbconn);

        return $response;
}

function preprocess_data($data)
{
    $data = trim($data);

    if($data == 'true')
        return 't';
    if($data == 'false')
        return 'f';

    return $data;
}


function timeToValue($time)
{
	$sources_time = explode(":", explode(" ", $time)[1]);
	$second       = intval($sources_time[2]);
	$minute       = intval($sources_time[1]);
	$hour         = intval($sources_time[0]);
	$allSeconds   = $second + $minute * 60 + $hour * 3600;

	return $allSeconds / 86400;
}

function _sql($query) {
	$log  = "postgres";
	$pass = "123456";
	$host = "localhost";
	return sql_user($host, "smartHack", "5432", $log, $pass, $query);
}

function amountRooms() {
	return _sql("SELECT count(*) FROM public.rooms WHERE name NOT LIKE 'Бойлерная'")[0]["count"];
}

?>