<?php
include "Server/functions.php";
?>

<html>
<head>
    <title>
        Умный дом. Нейросеть.
    </title>
    <script type="text/javascript" src="http://code.jquery.com/jquery-2.2.4.min.js"></script>
    <script type="text/javascript" src="http://code.jquery.com/jquery-2.2.4.js"></script>
    <link href="custom.css" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap-theme.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
</head>
<body>
<h2 align="center" class="title">Расположение комнат</h2>

<div class="tabbable"> <!-- Only required for left/right tabs -->
    <ul class="nav nav-tabs">
        <li class="active"><a href="#tab1" data-toggle="tab">Эконом-режим</a></li>
        <li><a href="#tab2" data-toggle="tab">Комфорт-режим</a></li>
    </ul>
    <div class="tab-content">
        <div class="tab-pane active" id="tab1">
            <p>

            <div class="main">
                <div class="row">

			        <?php
			        $amountSensor = amountSensors();
			        //$amountSensor = 2;

			        for ($i = 0; $i < $amountSensor; $i++)
			        {
				        ?>
                        <div class="col-md-12">
					        <?php echo 'Комната'.($i + 1); ?>
                        </div>
				        <?php
			        }
			        ?>
                </div>
            </div>

            </p>
        </div>
        <div class="tab-pane" id="tab2">
            <p>Привет, я в Разделе 2.</p>
        </div>
    </div>
</div>


<!--<div class="main">
    <div class="row">

        <?php
		$amountSensor = amountSensors();
		//$amountSensor = 2;

		for ($i = 0; $i < $amountSensor; $i++)
		{
			?>
            <div class="col-md-12">
                <?php echo 'Комната'.($i + 1); ?>
            </div>
			<?php
		}
		?>
    </div>
</div>
-->
</body>
</html>