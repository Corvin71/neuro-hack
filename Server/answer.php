<?php

include "functions.php";

if (isset($_POST["ans"])) {
    _sql("INSERT INTO public.logs(log) VALUES('" .$_POST["ans"] ."')");
}


?>
