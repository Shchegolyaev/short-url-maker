# Генератор сокращенных ссылок
Cервис для создания сокращенной формы передаваемых URL и анализа активности их использования.
## Steps to run:
1. Run Docker-compose
```
docker-compose up --build
  ```
2. Apply migrations
```angular2html
docker exec backend alembic upgrade head
```
3. Go to docs
```angular2html
http://127.0.0.1:8001/api/openapi
```
___________________

## Описание

 **http**-сервис, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080`.


<details>
<summary> Список эндпойнтов </summary>

1. Получить сокращенный вариант переданного URL
```python
POST /
```

Request
```json
https://...
```

Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`.


2. Вернуть оригинальный URL
```python
GET /<url_id>
```
Метод принимает в качестве параметра идентификатор сокращенного URL и возвращает ответ с кодом `307` и оригинальным URL в заголовке `Location`.

3. Вернуть статус использования URL
```python
GET /<url_id>/status?[full-info]&&[max-result=10]&&[offset=0]
```
Метод принимает в качестве параметра идентификатор сокращенного URL и возвращает информацию о количестве переходов, совершенных по ссылке.

В ответе может содержаться как общее количество совершенных переходов, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
- время перехода/использования ссылки;
- информация о клиенте, выполнившем запрос;

</details>



### Дополнительные возможности:

- Метод `GET /ping`, который возвращает информацию о статусе доступности БД.
- Возможность "удаления" сохраненного URL. Запись должна оставаться, но помечаться как удаленная. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.

-  **middlware**, блокирующий доступ к сервису запросов из запрещенных подсетей (black list).
