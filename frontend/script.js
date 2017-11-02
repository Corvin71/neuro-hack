var text = 'Войти в комнату';
var text2 = 'Выйти из комнаты';
var check = true;
var stateTimer = false;
var Temperature = 0;


function SendGet() {
    $.getJSON("Server/data_collection.php?get_rooms=1", function (data) {
        var items = "<thead><tr><th  class='text-center'>Название комнаты</th><th class='text-center'>Показания нейросети</th><th   class='text-center'>Температура</th><th colspan='2'  class='text-center'>Действие</th></tr></thead>";
        $.each(data, function (key, value) {
            items += "<tr><td>" + value + "</td><td><div class='demo-1'>" +
                "<div class='bar' id='loads" + parseInt(key + 1) + "_1" + "'>" +
                "<i class='sphere'></i>" +
                "</div>" +
                "<div id='inf" + parseInt(key + 1) + "_1" +"'>Показания нейросети" + "</div>" +
                "</div>" + "</td>" +
                "<td>" +
                "<input id='inp" + parseInt(key + 1) + "_1" + "' type='range' min='0' max='45' step='0.1' value='19' oninput='OnInput(this)'><br><span id='spn" + parseInt(key + 1) + "_1" +  "'></span></td>" +
                "<td><button class='btn btn-info' id='" + parseInt(key + 1) + "_1" + "' onclick='Test(this)'>Войти в комнату</button></td></tr>";
        });
        items += "<tr><td>Бойлерная (положение ручки бойлера)</td><td colspan='3'><input id='gas' type='range' min='0' max='1' step='0.01' value='0.3' oninput='OnInputGas(this)'><span id='spnGas'>" +
            "</span></td></tr>";
        $(".rooms").html(items)
    });
}

function Test(me) {
    //Смена класса у кнопки.
    document.getElementById(("inf" + me.id).toString()).innerText = '';
    document.getElementById(("loads" + me.id).toString()).style.display = "block";

    me.disable = true;
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

    //Проверка переключателя.
    _elSwitchMode = document.getElementById("c");
    _state = '';

    if (_elSwitchMode.checked)
        _state = 't';
    else
        _state = 'f';

    //Запуск таймера.
    StartTimer(me, _state);

    $.get("Server/data_collection.php?state_neuron=" + me.value + "&state_mode=" + _state, function(data){
        document.getElementById(("loads" + me.id).toString()).style.display = "none";
        $("#inf" + me.id).html(data)
    });

    me.disable = false;
}

function OnInput(item) {
    var _realId = (item.id.substr(3, item.id.length));
    document.getElementById(('spn' + _realId).toString()).innerText = (document.getElementById(item.id).value +" °C").toString();
}

function OnInputGas(item) {
    document.getElementById(('spnGas').toString()).innerText = (document.getElementById(item.id).value).toString();
}

function StartTimer(_el, state) {
    if (!stateTimer) {
        setInterval(function () {
            var startTemperature = document.getElementById('inp' + _el.id).value;

            $.get("Server/data_collection.php?state_neuron=" + _el.value + "&state_mode=" + state + "&startTemp=" + startTemperature +
                "&room_id=" + me.id.substr(2, me.id.length), function(data){
                document.getElementById(("loads" + me.id).toString()).style.display = "none";
                $("#inf" + me.id).html(data)
            });
        }, 6000);

        stateTimer = !stateTimer;
    }
}

