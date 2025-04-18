<h1>TableReservation</h1>

<h3>Методы API.</h3>

<h4>Столики:</h4>
<h5>    GET /tables/ — список всех столиков</h5>
<h5>    POST /tables/ — создать новый столик</h5>
<h5>    DELETE /tables/{id} — удалить столик по id</h5>
<h5>Пример входных данных для POST /tables/</h5>
{
    "name": "Новый столик",
    "seats": 4,
    "location": "Терраса"
}

<h4>Бронь:<h4>
<h5>    GET /reservations/ — список всех броней</h5>
<h5>    POST /reservations/ — создать новую бронь</h5>
<h5>    DELETE /reservations/{id} — удалить бронь по id</h5>
<h5>Пример входных данных для POST /reservations/</h5>
{
  "customer_name": "Иван Иванов",
  "reservation_time": "2023-06-15T19:00:00Z",
  "duration_minutes": 90,
  "table_id": 1
}


<h5>API позволяет создавать регистрировать/удалять столики и регистрировать/удалять бронь для них.
При пересечении новой брони с уже существующей, будет получено исключение с соответствующем текстом.</h5>
<h5>Для запуска приложения требуется файл с переменными окружения .env для подключения к базе данных. Данные в этот файл необходимо добавить по образцу
из файла .env.example</h5>
<h5>API запускается в контейнере, командой: docker-compose up</h5>
<h5>Стоит упомянуть что для запуска API в docker контейнере, в .env хост следует указать как databasetb, а порт как 5432</h5>
<h5>В то время как для локального запуска хост будет 127.0.0.1 а порт 6432</h5>
