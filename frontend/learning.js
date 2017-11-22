var serverAddress = "../Server/data_collection.php";
var statStartLearning = "";

function onLoadPage() {
    changeStateButton();
    //Скрываем кнопку "Продолжить обучение"
    if (!statStartLearning)
        $('.continueLearn')["0"].style.display = "none";

    loadInfoLearningSource();
    loadInfoLearningStats();
}

//Инициализация таблицы выгрзки обучающей выборки.
function loadInfoLearningSource() {
    $('#data-table').dataTable({
        "processing": true,
        "serverSide": true,
        'ajax': serverAddress + "?get_learning_selection=1",
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
        ],
        language: {
            "processing": "Подождите...",
            "search": "Поиск:",
            "lengthMenu": "Показать _MENU_ записей",
            "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Записи с 0 до 0 из 0 записей",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
            "infoPostFix": "",
            "loadingRecords": "Загрузка записей...",
            "zeroRecords": "Записи отсутствуют.",
            "emptyTable": "В таблице отсутствуют данные",
            "paginate": {
                "first": "Первая",
                "previous": "Предыдущая",
                "next": "Следующая",
                "last": "Последняя"
            },
            "aria": {
                "sortAscending": ": активировать для сортировки столбца по возрастанию",
                "sortDescending": ": активировать для сортировки столбца по убыванию"
            }
        }
    });
}

//Инициализация таблицы статистики процесса обучения.
function loadInfoLearningStats() {
    $('#data-table-network').dataTable({
        "processing": true,
        "serverSide": true,
        'ajax': serverAddress + "?get_info_learn=1",
        'columns': [
            {"data" : "Дата"},
            {"data" : "Кол-во оставшихся дней"},
            {"data" : "Ошибка сети 'Комфорт'"},
            {"data" : "Ошибка сети 'Эконом'"}
        ],
        language: {
            "processing": "Подождите...",
            "search": "Поиск:",
            "lengthMenu": "Показать _MENU_ записей",
            "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Записи с 0 до 0 из 0 записей",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
            "infoPostFix": "",
            "loadingRecords": "Загрузка записей...",
            "zeroRecords": "Записи отсутствуют.",
            "emptyTable": "В таблице отсутствуют данные",
            "paginate": {
                "first": "Первая",
                "previous": "Предыдущая",
                "next": "Следующая",
                "last": "Последняя"
            },
            "aria": {
                "sortAscending": ": активировать для сортировки столбца по возрастанию",
                "sortDescending": ": активировать для сортировки столбца по убыванию"
            }
        }
    });
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
    //$('#data-table').load(serverAddress + "?get_learning_selection=1&totalDisplayRecords=2", function (answer) {
    $('.status-load').text('Производится загрузка данных...');
    $('.status-load').text('Данные упешно загружены');
    $('.status-load').text('');
    //});
}


