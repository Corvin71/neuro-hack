var serverAddress = "../Server/data_collection.php";
var statStartLearning = "";

function onLoadPage() {
    changeStateButton();
    //Скрываем кнопку "Продолжить обучение"
    if (!statStartLearning)
        $('.continueLearn')["0"].style.display = "none";
}

function startLearn() {
    changeStateButton();

    if ((statStartLearning === "") || (statStartLearning === "f")) {
        $.getJSON(serverAddress + "?info_learn=1", changeStateButton());
    }
    else if (statStartLearning === "t") {
        $.getJSON(serverAddress + "?info_learn=2", changeStateButton());
    }

    //Снять комментарий.
    /*$('.info').innerText = "Осуществляется запуск генерации обучающей выборки...";
    //Запрос к серверу для запуска обучающего скрипта.
    $.getJSON(serverAddress + "?start_learning=1", function(data) {
        $('.info').innerText = "Осуществляется запуск обучения сети...";
        //Запуск скрипта на обучение сети.
        $.getJSON(serverAddress + "?start_learning=2", function (result) {
            $('.info').innerText = "Сеть успешно обучена!!!";
        });
    });*/
}

function changeStateButton() {
    //Стучимся на сервер и смотрим в какой стадии обучение.
    $.getJSON(serverAddress + "?info_learn=0", function (result) {
        console.log(result);
        // Обучение прервано
        if (result === "f") {
            //Случай с прерванным обучением.
            $('.startStopLearn').html('Начать обучение заново');
            $('.continueLearn').css('display', 'block');
            $('.startStopLearn')["0"].classList.remove("btn-info");
            $('.startStopLearn')["0"].classList.add("btn-default");
        }
        // Обучение завершено
        else if (result === "") {
            $('.startStopLearn').html('Начать обучение заново');
            $('.continueLearn').css('display', 'none');
            $('.startStopLearn')["0"].classList.remove("btn-default");
            $('.startStopLearn')["0"].classList.add("btn-info");
        }
        // Обучение в процессе
        else if (result === "t") {
            $('.startStopLearn').html('Прервать обучение');
            $('.continueLearn').css('display', 'none');
            $('.startStopLearn')["0"].classList.remove("btn-info");
        }

        statStartLearning = result;
    });
}

//Продолжить обучение.
function continueLearn() {
    changeStateButton();
    $.getJSON(serverAddress + "?info_learn=1", changeStateButton());
}

function loadInfoSelection() {
    $('.info-selection').load(serverAddress + "?get_learning_selection=1&totalDisplayRecords=2", function (answer) {
        $('.data-table-info').dataTable({
            'ajax': {
                "data"   : answer
            },
            'columns': [
                {"data" : "Дата"},
                {"data" : "Комната"},
                {"data" : "Расход газа"},
                {"data" : "Регулятор газа"},
                {"data" : "Температура по Цельсию"},
                {"data" : "Регулятор кондиционера"},
                {"data" : "Регулятор радиатора"},
                {"data" : "Расход энергии"},
                {"data" : "Датчик движения"}
            ]
        });
        //$('.info-selection').innerHTML = answer;
    });
}


