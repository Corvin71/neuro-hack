﻿<?php

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
	$result = array();
	$amountRooms = _sql("SELECT * FROM public.rooms WHERE name NOT LIKE 'Бойлерная'");
	for ($i = 0; $i < count($amountRooms); $i++)
	{
		$result[$i] = $amountRooms[$i]["name"];
	}

	echo json_encode($result, JSON_UNESCAPED_UNICODE);
}

//Запускает или останавливает нейросеть.
if (isset($_GET["state_neuron"]) && isset($_GET["id_room"])) {
	//Здесь действие для деактивации сети.
	if ($_GET["state_neuron"] == "t") {

	}
	//А здесь действие для активации сети.
	else if ($_GET["state_neuron"] == "f") {
		$result = exec("cmd");
	}
}

//Запись логов в базу данных.
if (isset($_POST["log"]) && ($_POST["log"] != ""))
{
	_sql("INSERT INTO public.logs(log) VALUES ('" . $_POST["log"] . "')");
}