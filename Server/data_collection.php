﻿<?php
header('Access-Control-Allow-Origin: *');
include "functions.php";

//Возвращает данные для обучения в формате JSON.
if (isset($_GET["is_learning"]))
{
	$statusSensors = _sql("SELECT * FROM public.status_sensors WHERE date LIKE ('" . $_GET["is_learning"] . "%') ORDER BY date, room_id ASC ");
	$resultArray   = array();
	if (count($statusSensors) != 0)
	{
		$date      = $statusSensors[0]["date"];
		$tempArray = array();
		$index     = 3;
		$testIndex = 0;

		foreach ($statusSensors as $sensor)
		{
			if ($sensor["date"] == $date)
			{
				if ($sensor["consum_gas"] != "")
				{

					$timeInSeconds = timeToValue($sensor["date"]);

					$tempArray[0] = round((float) $timeInSeconds, 3);
					$index++;
					$tempArray[1] = round((float) $sensor["consum_gas"], 3);
					$tempArray[2] = round((float) $sensor["twister_gas"], 3);
				}
				else
				{
					$tempArray[$index] = round(((float) $sensor["celsium"]) / 45.0, 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["smove"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["twister_cold"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["twister_radiator"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["energy"], 3);
					$index++;
				}
			}
			else
			{
				if (count($tempArray) != 0)
				{
					ksort($tempArray);
					$resultArray[count($resultArray)] = $tempArray;
				}

				unset($tempArray);
				$tempArray     = array();
				$index         = 3;
				$date          = $sensor["date"];
				$timeInSeconds = timeToValue($sensor["date"]);

				$tempArray[0] = round((float) $timeInSeconds, 3);

				if ($sensor["consum_gas"] != "")
				{
					$tempArray[$index] = round((float) $sensor["consum_gas"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["twister_gas"], 3);
					$index++;
				}
				else
				{
					$tempArray[$index] = round(((float) $sensor["celsium"]) / 45.0, 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["smove"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["twister_cold"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["twister_radiator"], 3);
					$index++;
					$tempArray[$index] = round((float) $sensor["energy"], 3);
					$index++;
				}
			}
		}
	}

	echo json_encode($resultArray, JSON_UNESCAPED_UNICODE);
}

//Возвращает количество комнат.
if (isset($_GET["how_rooms"]))
{
	echo amountRooms();
}

//Запрос комнат с названиями и идентификаторами в JSON-формате.
if (isset($_GET["get_rooms"]))
{
	$result      = array();
	$amountRooms = _sql("SELECT * FROM public.rooms WHERE name NOT LIKE 'Бойлерная'");
	for ($i = 0; $i < count($amountRooms); $i++)
	{
		$result[$i] = $amountRooms[$i]["name"];
	}

	echo json_encode($result, JSON_UNESCAPED_UNICODE);
}

//TODO - сделать принятие параметров get: p, g, t
// p - массив присутствия, t - температуры, g - крутилка газа.
//Server/data_collection.php?p=f,t,t,t,t&t=19,19,19,19,19&g=0.3
//if

// Запуск нейронной сети в рабочем режиме.
if(isset($_GET["start_network"])) {
	if($_GET["is_econom"])
	{
		// Дёргаем Питона для эконома
		exec("python ../neurohouse.py -e");
		//print_r($output);
	}
	else {
		// Дёргаем Питона для комфорта
		exec("python ../neurohouse.py -c");
	}
	// Здесь дёргаем последнюю запись крутилок из БД и возвращаем в json'е
	$result = _sql("SELECT * FROM public.logs ORDER BY date DESC LIMIT 1");
	$answer = json_decode($result[0]["log"]);
	echo json_encode($answer, JSON_UNESCAPED_UNICODE);
}


//Запуск скрипта обучающей выборки python.
if (isset($_GET["start_learning"])) {
	if ($_GET["start_learning"] == 1) {
		//Дергаем Питон для генерации обучающей выборки.
		//СНЯТЬ КОММЕНТАРИЙ.
		exec("python ../database/generate_data.py");
	}
	elseif ($_GET["start_learning"] == 2) {
		//Дергаем Питона для запуска процесса обучения.
		//СНЯТЬ КОММЕНТАРИЙ.
		exec("python ../neurohouse.py --learn-only");
	}
}

if (isset($_GET["info_learn"])) {
	//Если принят 0 - вернуть из БД, запущено ли обучение, 1 - запустить обучение, 2 - остановить обучение.
	switch ($_GET["info_learn"]) {
		case "0":
			$result = _sql("SELECT state FROM public.is_learning LIMIT 1")[0]["state"];
			echo json_encode($result, JSON_UNESCAPED_UNICODE);
			break;
		case "1":
			_sql("UPDATE public.is_learning SET state = true");
			break;
		case "2":
			_sql("UPDATE public.is_learning SET state = false");
			break;
	}
}

//Возвращает данные по выборке для обучения.
if (isset($_GET["get_learning_selection"])) {
	$resultSql = _sql("SELECT * FROM public.info_learning LIMIT " .$_GET["length"] ." OFFSET " .$_GET["start"] .";");

	$iTotalRecords = _sql("SELECT count(*) FROM public.status_sensors")[0]["count"];

	$newResult = array("draw" => isset ( $_GET['draw'] ) ? intval( $_GET['draw'] ) : 0,
	                   "recordsTotal" => intval($iTotalRecords),
	                   "data" => $resultSql);

	echo json_encode($newResult, JSON_UNESCAPED_UNICODE);
}

//Получение статистики процесса обучения.
if (isset($_GET["get_info_learn"])) {
	$resultSql = _sql("SELECT * FROM public.view_info_learn LIMIT " .$_GET["length"] ." OFFSET " .$_GET["start"] .";");

	$iTotalRecords = _sql("SELECT count(*) FROM public.info_learn")[0]["count"];

	$newResult = array("draw" => isset ( $_GET['draw'] ) ? intval( $_GET['draw'] ) : 0,
	                   "recordsTotal" => intval($iTotalRecords),
	                   "data" => $resultSql);

	echo json_encode($newResult, JSON_UNESCAPED_UNICODE);
}