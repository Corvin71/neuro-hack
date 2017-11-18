<?php

include "functions.php";

if (isset($_POST["ans"])) {
    _sql("INSERT INTO public.logs(log) VALUES('" .$_POST["ans"] ."')");
}

//Принятие данных от python скрипта (обучающая выборка) и проталкивание их в БД.
if (isset($_POST["ins_db"])) {
    $test = "";
    _sql($_POST["ins_db"]);
}


?>
