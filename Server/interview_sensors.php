<?php

include "functions.php";

function start_interview() {
	$arraySensors = _sql("SELECT * FROM public.sensors");

	// Для реальных задач.
	// Проход по датчикам.
	foreach ($arraySensors as $sensor) {
		// Опрашиваем каждый из датчиков по ip не менее трех раз.

		// Результат опроса датчика.
		$result = '';
		for($i = 0; $i < 3; $i++) {
			// Ответ от датчика пришел или нет.
			$result = file_get_contents("http://" .$sensor["ip"]);

			if (strlen($result) > 0) {
				// Возможно тут выполняется проверка на корректность данных.
				break;
			}
			else {
				sleep(5);
			}
		}

		// Если успешен опрос, то...
		if (strlen($result) > 0) {
			mb_internal_encoding("UTF-8");
			$end = json_decode($result, true);
			// Формат ответа датчика {"type": "Celsius", "value": "25"};
			// Проталкиваем в БД.
			_sql("INSERT INTO public.status_sensors(" .mb_substr($end[]) .") VALUES('" .$end["value"] ."')");
		}
	}



	// Эмуляция опроса датчиков.
}

start_interview();

?>