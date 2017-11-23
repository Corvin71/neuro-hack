var text = 'Войти в комнату';
var text2 = 'Выйти из комнаты';
var check = true;
var timerIsActive = false;
var temperature = [];

var serverAddress = "Server/data_collection.php";

var countOfActiveRooms = 0;
var timerID = 0;

function SendGet() {
    $.getJSON(serverAddress + "?get_rooms=1", function (data) {
        var items = "<thead><tr><th class='text-center'>Название комнаты</th>" +
            "<th class='text-center'>Регулятор кондиционера<br>действ.|ожид.</th>" +
            "<th class='text-center'>Регулятор радиатора<br>действ.|ожид.</th>" +
            "<th class='text-center'>Температура (°C)</th>" +
            "<th colspan='2' class='text-center'>Присутствие людей</th></tr></thead>";
        $.each(data, function (key, value) {
            items += "<tr><td>" + value + "</td>" +
                "<td><div id='twister_conditioner" + parseInt(key) + "'>0 | 0</div></td>" +
                "<td><div id='twister_radiator" + parseInt(key) + "'>0 | 0</div></td>" +
                "<td><div id='temperature" + parseInt(key) + "'>0</div></td>" +
                "<td><div id='presents" + parseInt(key) + "'>нет</div></td></tr>";
        });
        items += "<tr><td><b>Положение регулятора бойлера</b></td><td><div id='twister_gas'>0</div></td></tr>";
        items += "<tr><td><b>Максимальный расход энергии на комнату (Вт)</b></td><td><div id='energy'>2000</div></td></tr>";
        $(".rooms").html(items)
    })
    .fail(function() {
        $(".message").html("Невозможно получить данные. Для повторной попытки обновите страницу.");
    })
}

function getNetResult() {
    var request = serverAddress + "?start_network=1";
    // Проверка переключателя
    if($("#c")[0].checked) {
        request += '&is_econom=1';
    }

    $.getJSON(request, function(data) {
        alert(data);
        /*var j = 1;
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
        });*/
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

function StartTimer() {
    if (!timerIsActive) {
        timerID = setInterval(function () {
            getNetResult();
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

StartTimer();
