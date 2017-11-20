var serverAddress = "../Server/data_collection.php";
var statStartLearning = false;

function onLoadPage() {
    startLearn();
    //Скрываем кнопку "Продолжить обучение"
    if (!statStartLearning)
        $('.continueLearn')["0"].style.display = "none";
}

function startLearn() {
    //Смена надписи кнопки и класса.
    //Стучимся на сервер и смотрим в какой стадии обучение.
    $.getJSON(serverAddress + "?info_learn=0", function (result) {
        console.log(result);
        if (result === "f") {
            //Случай с прерванным обучением.
            $('.startStopLearn')["0"].classList.remove("btn-info");
            $('.startStopLearn')["0"].classList.add("btn-default");
            statStartLearning = !statStartLearning; //true
            $('.startStopLearn')["0"].innerText = "Возобновить обучение";
            $('.continueLearn')["0"].style.display = "block";
        }
        else if (result === "") {
            $('.startStopLearn')["0"].innerText = "Перезапустить обучение";
            statStartLearning = !statStartLearning;
            $('.startStopLearn')["0"].classList.remove("btn-default");
            $('.startStopLearn')["0"].classList.add("btn-info");
        }
        else if (result === "t") {
            //Случай с прерванным обучением.
            $('.startStopLearn')["0"].classList.remove("btn-info");
            $('.startStopLearn')["0"].classList.add("btn-default");
            statStartLearning = !statStartLearning; //true
            $('.startStopLearn')["0"].innerText = "Прервать обучение";
            $('.continueLearn')["0"].style.display = "block";
        }
    });

    if (!statStartLearning) {
        //$('.startStopLearn').classList.add()
    }

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

//Продолжить обучение.
function continueLearn() {

}

