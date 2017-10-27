<?php

include "functions.php";

if (isset($_GET["is_learning"]))
{
	$statusSensors = _sql("SELECT * FROM public.status_sensors WHERE date LIKE ('" .$_GET["is_learning"] ."%') ORDER BY date, room_id ASC ");
	$resultArray = array();
	if (count($statusSensors) != 0) {
		$date =  $statusSensors[0]["date"];
		$tempArray = array();
		$index = 3;
		$testIndex =0;

		foreach ($statusSensors as $sensor) {
			if ($sensor["date"] == $date) {
				if ($sensor["consum_gas"] != "") {

					$timeInSeconds = timeToValue($sensor["date"]);

					$tempArray[0] = round((float) $timeInSeconds, 3);
					$index++;
					$tempArray[1] = round((float)$sensor["consum_gas"], 3);
					$tempArray[2] = round((float)$sensor["twister_gas"], 3);
				}
				else {
					$tempArray[$index] = round(((float)$sensor["celsium"]) / 45.0, 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["smove"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["twister_cold"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["twister_radiator"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["energy"], 3);
					$index++;
				}
			}
			else {
				if (count($tempArray) != 0) {
					ksort($tempArray);
					$resultArray[count($resultArray)] = $tempArray;
				}

				unset($tempArray);
				$tempArray = array();
				$index = 3;
				$date = $sensor["date"];
				$timeInSeconds = timeToValue($sensor["date"]);

				$tempArray[0] = round((float) $timeInSeconds, 3);

				if ($sensor["consum_gas"] != "") {
					$tempArray[$index] = round((float)$sensor["consum_gas"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["twister_gas"], 3);
					$index++;
				}
				else {
					$tempArray[$index] = round(((float)$sensor["celsium"]) / 45.0, 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["smove"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["twister_cold"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["twister_radiator"], 3);
					$index++;
					$tempArray[$index] = round((float)$sensor["energy"], 3);
					$index++;
				}
			}
		}
	}

	echo json_encode($resultArray, JSON_UNESCAPED_UNICODE);
}

if (isset($_GET["how_rooms"])) {
	echo 5;
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
