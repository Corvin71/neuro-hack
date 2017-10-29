[Bvar text = 'Войти в комнату';
var text2 = 'Выйти из комнаты';
var check = true;


function SendGet() {
    $.getJSON("Server/data_collection.php?get_rooms=1", function (data) {
        var items = "<thead><tr><th  class='text-center'>Название комнаты</th><th class='text-center'>Показания нейросети</th><th colspan='2'  class='text-center'>Действие</th></tr></thead>";
        $.each(data, function (key, value) {
            items += "<tr><td>" + value + "</td><td id='key" + parseInt(key + 1) + "_1"  + "'>Показания нейросети</td><td><button class='btn btn-info' id='" + parseInt(key + 1) + "_1" + "' onclick='Test(this)'>Войти в комнату</button></td></tr>";
        });
        $(".rooms").html(items)
    });
}

function Test(me) {
    //Смена класса у кнопки.
    if ((me.value === "t") || (me.value === "")) {
        me.classList.remove("btn-info");
        me.classList.add("btn-warning");
        me.innerText = text2;
        me.value = 'f';
    }
    else {
        me.classList.remove("btn-warning");
        me.classList.add("btn-info");
        me.innerText = text;
        check = true;
        me.value = 't';
    }

    $.get("Server/data_collection.php?state_neuron=" + me.value + "&id_room=" + me.id, function(data){ 
	$("#key" + me.id).html(data)
    });
}

