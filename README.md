###Запуск
```
git clone https://github.com/PitonX60/litebox.git
```

```
docker-compose up -d
```

```
http://127.0.0.1:8005
```

###Стек
- djnago 2.2.17;
- djnago rest framework;
- firebird;
- docker.

Выборе версии djnago исходил из ограничений пакета djnago-firebird. Он, к сожалению, не работает с djnago 3+.

### Описание

В коде показал различную работу View. Так для магазинов используется класс APIView, для товаров GenericAPIView (потомки), 
для документов ModelViewSet, а для endpoint-а авторизации использовал декоратор api_view, который позволяет обходить без 
создания класса вьюхи. 

В работе с сериализатором показал работу с встроенным сериализатором, с переопределенными методами create/update, 
использование транзакций для атомарного обновления записей.

Так же показал работу с несколькими сериализаторами в рамках одного класса вьюхи.

Создал пример использования <b>unut-тестов</b> с полным покрытием класс ShopView.

Начальное заполение БД реализовал через кастомную миграцию. 
##### Сложности

В качестве БД выбрал firebird и по фен-шую решил завернуть в докер не только саму БД но и весь djnago-прокет. Чтобы 
запустить его с минимальными действиями на любой платформе.

Из описания пакета https://github.com/maxirobaina/django-firebird:

```
This version of django-firebird is working with fbd [1], therefore it will work only with firebird 2.x and later. 
The stable version corresponds with django 2.2 and live into stable/2.2.x branch.
```

Версия 2.2a1 оказалась рабочей только частично. В условиях ТЗ указано, что нужно для документов использовать SQL-запросы,
с этим в django-firebird как раз связана первая проблема пакета. Для ее устранения я сделал форк оригинальной ветки и 
пофиксил ее. Как выяснилось дальше, проблема есть еще с выполнением unit-тестов. Эту 
проблему я фиксить не стал т.к. уже затратил значительно время на связку djnago-firebird-docker.

Тем не менее unit-тесты прогнать можно при локальном разворачивании проекта (или развернуть БД posgresql в докере место
firebird):

```
git clone https://github.com/PitonX60/litebox.git
cd litebox
python -m venv venv
```
Если windows:
```
venv\Scripts\activate
```
Если linux:
```
source venv/bin/activate
```

```
pip insatll -r requirements.txt
```

Далее в DATABASES в settings.py раскомментировать backends для sqlite3 и закомментировать  firebird.

Миграции:
```
python manage.py migrate
```

Запустить тест:
```
python manage.py test online_store.tests
```

---

Из-за этой связки и затраченного на нее время я, к сожалению, не успел реализовать все что задумывал. В частности:
- единицы товара;
- штрих-коды;
- router в urls;
- swagger;
- выложить на сервер, чтобы показать работу с CORS-ами.

Эти задачи находятся в той или иной степени начинания. 

###API

Т.к. в этом репозитории только бэк. Опишу частично реализованные интерфейсы

Авторизация:
```
curl -X POST "http://127.0.0.1:8005/api/login/" -H "Content-Type: application/json" -d '{"username": "admin", "password": "litebox1234"}'
```

Список магазинов
```
curl -X GET "http://127.0.0.1:8005/api/shops/" -H  "Content-Type: application/json" -H "Authorization: Token <токен полученный в api/login>"
```

Список документов:
```
curl -X GET "http://127.0.0.1:8005/api/docs/" -H  "Content-Type: application/json" -H "Authorization: Token <токен полученный в api/login>"
```

Полный список всех интерфейсов можно посмотреть в .api_request. Описанные там запросы будут работать в IDE PyCharm. 

Так же список интерфейсов можно посмотреть в swagger (но оттуда, как я уже писал выше, запустить не получится): 
 
http://127.0.0.1:8005/
http://127.0.0.1:8005/redoc/ 
