var text = 'Войти в комнату';
var text2 = 'Выйти из комнаты';
var check = true;
var timerIsActive = false;
var temperature = [];

var serverAddress = "../Server/data_collection.php";

var countOfActiveRooms = 0;
var timerID = 0;

function SendGet() {
    $.getJSON(serverAddress + "?get_rooms=1", function (data) {
        var items = "<thead><tr><th  class='text-center'>Название комнаты</th><th class='text-center'>Показания нейросети</th><th   class='text-center'>Температура</th><th colspan='2'  class='text-center'>Действие</th></tr></thead>";
        $.each(data, function (key, value) {
            items += "<tr><td>" + value + "</td><td><div class='demo-1'>" +
                "<div class='bar' id='loads" + parseInt(key + 1) + "_1" + "'>" +
                "<i class='sphere'></i>" +
                "</div>" +
                "<div id='inf" + parseInt(key + 1) + "_1" +"' class='inff'>0, 0" + "</div>" +
                "</div>" + "</td>" +
                "<td>" +
                "<input class='slid' id='inp" + parseInt(key + 1) + "_1" + "' type='range' min='0' max='45' step='0.1' value='19' oninput='OnInput(this)'><br><span id='spn" + parseInt(key + 1) + "_1" +  "'>19°C</span></td>" +
                "<td><button class='btn btn-info' id='" + parseInt(key + 1) + "_1" + "' onclick='Test(this)'>Войти в комнату</button></td></tr>";
                temperature.push(19);
        });
        items += "<tr><td>Бойлерная (положение ручки бойлера)</td><td colspan='3'><input id='gas' class='gaas' type='range' min='0' max='1' step='0.01' value='0.3' oninput='OnInputGas(this)'><span id='spnGas'>" +
            "0.3</span></td></tr>";
        $(".rooms").html(items)
    })
    .fail(function() {
        $(".message").html("Невозможно получить данные. Для повторной попытки обновите страницу.");
    })
}

function getNetResult(me) {
    // Формируем строку запроса
    var request = serverAddress + "?p=";
    $('.btn').each(function(i, elem) {
        request += elem.value !== '' ? elem.value + ',' : 't,';
    });
    request = request.substr(0, request.length - 1) + '&t=';
    $('.slid').each(function(i, elem) {
        request += elem.value - temperature[i] + ',';
        temperature[i] = elem.value;
    });
    request = request.substr(0, request.length - 1);
    request += '&g=' + document.getElementById('gas').value;
    // Проверка переключателя
    if($("#c")[0].checked) {
        request += '&is_econom=1';
    }

    $.getJSON(request, function(data) {
        var j = 1;
        var temp = '';
        if ($("#c")[0].checked && data.length % 2 != 0) {
            $("#gas")[0].value = data[data.length - 1];
            $("#spnGas").text(data[data.length - 1]);
        }

        $('.bar').each(function(i, item) {
            item.style.display = "none";
        });

        $.each(data, function(i, item) {
            temp += item + '; ';
            if(i % 2 != 0) {
                $("#inf" + j + "_1").html(temp);
                temp = '';
                j++;
            }
        });
    });
}

function Test(me) {
    //Смена класса у кнопки.

    $('.inff').each(function(i, item) {
        item.innerText = '';
    });
    $('.bar').each(function(i, item) {
        item.style.display = "block";
    });
    //document.getElementById(("inf" + me.id).toString()).innerText = '';
    //document.getElementById(("loads" + me.id).toString()).style.display = "block";

    me.disable = true;
    if ((me.value === "t") || (me.value === "")) {
        // Осуществляется вход в комнату
        me.classList.remove("btn-info");
        me.classList.add("btn-warning");
        me.innerText = text2;
        me.value = 'f';
        countOfActiveRooms++;
    }
    else {
        // Осуществляется выход из комнаты
        me.classList.remove("btn-warning");
        me.classList.add("btn-info");
        me.innerText = text;
        check = true;
        me.value = 't';
        countOfActiveRooms--;
    }

    //Запуск таймера.
    if(countOfActiveRooms > 0)
        StartTimer(me);
    else
        StopTimer();

    /*$.get("Server/data_collection.php?state_neuron=" + me.value + "&is_econom=" + _state, function(data){
        document.getElementById(("loads" + me.id).toString()).style.display = "none";
        $("#inf" + me.id).html(data)
    }); */
    me.disable = false;
}

function OnInput(item) {
    var _realId = (item.id.substr(3, item.id.length));
    document.getElementById(('spn' + _realId).toString()).innerText = (document.getElementById(item.id).value +"°C").toString();
}

function OnInputGas(item) {
    document.getElementById(('spnGas').toString()).innerText = (document.getElementById(item.id).value).toString();
}

function StartTimer(me) {
    if (!timerIsActive) {
        timerID = setInterval(function () {
            getNetResult(me);
        }, 6000);

        timerIsActive = true;
    }
}

function StopTimer() {
    if(timerID !== 0) {
        clearInterval(timerID);
        timerIsActive = false;
        timerID = 0;
    }
}

function StartLearning() {
    //Открытие новой вкладки.
    window.open("learning.html");
}