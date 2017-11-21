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

//Принятие данных об обучении и кол-ве оставшихся дней.
if (isset($_POST["log"])) {
    $str = $_POST["log"];
    //$str = "2017-11-22 01:25:17.917000: Epoch complete. Errors: comfort: 0.210927610801; econom: 0.0704210262057; left (days): 1";

    if (strripos($str, "Epoch complete") !== false) {
        $str = str_replace("Epoch complete. Errors: ", "", $str);
        $firstArray = explode(";", $str);

        $errorComfort = explode(" ", $firstArray[0])[3];

        $errorEconom = explode(":", $firstArray[1])[1];
        $leftDays = explode(":", $firstArray[2])[1];

        //Проталкивание в базу.
        _sql("INSERT INTO public.info_learn(amount_day, error_comfort, error_econom) VALUES (" .$leftDays .", " .$errorComfort .", "  .$errorEconom .")");
    }

    //Если что, добавить в БД остальные логи.
}


?>
