# Тестовое задание

Установка виртуального окружения
```
mkdir app
cd app
virtualenv venv
source venv/bin/activate
```

Deploy
```
git clone https://github.com/KozlovDmitry/testTask
cd testTask
pip install -r requirements.txt
python manage.py makemigrations interview
python manage.py migrate
python manage.py createsuperuser                        // login и password потребуются для выполнения запросов по создания/изменеию/удалению вопросов/опросов
python manage.py runserver
```

# Инструкция API
## Api с правами администратора
Все запросы для адимн-действий выполняются с login/password созданного superuser

Пример:
curl -u adimn_login:admin_password localhost:8000/api/quiz/

GET /api/quiz/                                          -   возвращает список всех созданных опросов
POST /api/quiz/                                         -   создание опроса
Пример тела запроса:
```
{
	"name": "test quiz",
	"description": "Sth that describe it",
	"start_date": "2021-01-01 01:00",
	"end_date": "2022-01-01 01:00"
}
```
Возвращает созданный опрос или сответствующую ошибку

GET/PUT/DELETE /api/quiz/id/                            - просмотр/изменение/удаление опроса. Для изменения опроса тело запроса аналогичное как для создания опроса
                                                          только время создания менять нельзя


GET /api/question/                                      - список всех вопросов
POST /api/question/                                     - создание воопроса
Пример тела запроса:
```
{
    "quiz": [1],
    "text": "What is your name?",
    "type": "ответ текстом"
}
```
Возвращает созданный вопрос или сответствующую ошибку

GET/PUT/DELETE /api/question/id/                        - просмотр/изменение/удаление вопсроса. 


## Api без прав администратора(авторизация не нужна)

GET /api/availablequiz/                                 - возвращает активные опросы(текущее время между временем начала и окончания опроса)
GET /api/availablequiz/id/                              - возвращает список вопросов в активном опросе

POST /api/passquiz/                                     - прохождение теста
Пример тела запроса:
```
{
    "user_id": 111,
    "quiz": 1,
    "answers": [
    	{
    		"question": 1,
    		"answer": 1
    	},
    	    	{
    		"question": 2,
    		"answer": 2
    	}
    	]
}
```

GET /api/passedquiz/user_id/                            - возвращает пройденые пользователем опросы

