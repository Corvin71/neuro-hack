var serverAddress = "../Server/data_collection.php";
var statStartLearning = 0;

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
        // Обучение прервано
        if (result === "f") {
            //Случай с прерванным обучением.
            $('.startStopLearn').html('Начать обучение заново');
            $('.continueLearn').css('display', 'block');
            $('.startStopLearn')["0"].classList.remove("btn-info");
            $('.startStopLearn')["0"].classList.add("btn-default");
            statStartLearning = 0;
        }
        // Обучение завершено
        else if (result === "") {
            $('.startStopLearn').html('Начать обучение заново');
            $('.continueLearn').css('display', 'none');            
            $('.startStopLearn')["0"].classList.remove("btn-default");
            $('.startStopLearn')["0"].classList.add("btn-info");
            statStartLearning = 1;
        }
        // Обучение в процессе
        else if (result === "t") {
            $('.startStopLearn').html('Прервать обучение');
            $('.continueLearn').css('display', 'none');
            $('.startStopLearn')["0"].classList.remove("btn-info");
            statStartLearning = 5;
        }
    });

    switch(statStartLearning){
        // 0 === false
        case 0:
            break;
        // 1 === null
        case 1:
            break;
        // 5 === true
        case 5:
            break;
        default:
            alert('хер');
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

