var serverAddress = "../Server/data_collection.php";

function load() {
    $('.info').innerText = "Осуществляется запуск генерации обучающей выборки...";
    //Запрос к серверу для запуска обучающего скрипта.
    $.getJSON(serverAddress + "?start_learning=1", function(data) {
        $('.info').innerText = "Осуществляется запуск обучения сети...";
        //Запуск скрипта на обучение сети.
        $.getJSON(serverAddress + "?start_learning=2", function (result) {
            $('.info').innerText = "Сеть успешно обучена!!!";
        });
    });
}