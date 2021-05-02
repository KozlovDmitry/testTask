# Приложение Interview
Требования к системе:

Python 3.7 и новее, git, venv

Инструкция по запуску(ubuntu/macOS):
```
mkdir app
cd app
virtualenv venv
source venv/bin/activate
git init
git pull https://github.com/KozlovDmitry/testTask
pip install -r requirements.txt
python manage.py runserver
```
>В БД созданы несколько тестовых записей и учетка администратора(admin/admin), если они не требуются то выполнить:
```
rm db.sqlite3
rm -r research/interview/migrations/
python manage.py makemigrations interview
python manage.py migrate
python manage.py createsuperuser
```

# Инструкция API
По умолчанию сервер создаюётся на адресе localhost:8000
Создана и настроена admin-пенель django на адресе localhost:8000/admin

## Api с правами администратора
Просмотр типов вопросов:

GET - /api/questiontype

пример ответа
```
[
    {
        "id": 5,
        "type": "ответ с выбором одного варианта"
    },
    {
        "id": 6,
        "type": "ответ с выбором нескольких вариантов"
    },
    {
        "id": 13,
        "type": "ответ текстом"
    }
]
```

Создание типа вопроса:

POST - /api/questiontype

пример запроса:

```
{
    "type": "ответ текстом"
}
```

Просмотр/удаление типа вопроса:

GET/DELETE - /api/questiontype/{id_вопроса}


Просмотр вариантов ответа:

GET - /api/questionoption


Создание варианта ответа:

POST - /api/questionoption

Пример запроса:
```
{
    "name": "Piano"
}
```

Просмотр/удаление варианта ответа:

GET/DELETE - /api/questionoption/{id_варианта_ответа}


Просмотр вопросов:

GET - api/question

Создание вопроса:

POST - api/question

Пример запроса:
```
{
    "name": "Surname?",                                     //Обязательное поле
    "type": {
        "type":  "ответ с выбором нескольких вариантов"     //Обязательное поле
    },
    "question_option": [                                    //Обязательное поле только при типах вопроса "ответ с выбором одного варианта" 
      {                                                     //и "ответ с выбором нескольких вариантов"
        "name": "Ivanov"                                    //если будут переданы варианты, которых нет, они будут созданы
      }
],
    "quiz": [18]                                            //Необязательное поле. Принимает список id опросов, к которым будет относиться данный вопрос
}
```

Просмотр/удаление/изменени вопроса:

GET/DELETE/PUT - api/question/{id_вопрса}

```
Для PUT обязательных полей нет. Запрос формируется аналогично примеру в POST
```

Просмотр опросов:

GET - api/quiz

Создание опроса:

POST - api/quiz

Пример запроса
```
{
    "name": "Second Quiz",                // Обязательно поле
    "start_date": "2021-05-02T12:00",     // Обязательное поле(изменить после создания нельзя) - формат YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]
    "end_date": null,                     // Необязательное поле. Формат YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]
    "active": false,                      // Обязательное поле (default=False)
    "description": "Second Quiz",         // Необязательное поле
    "questions": [30]                     // Необязательное поле. Принимает список id вопросов, которые будут относиться к данному опросу
}
```

Просмотр/удаление/изменение опроса:

GET/DELETE/PUT - api/quiz/{id_опроса}

```
Для PUT обязательных полей нет. Запрос аналогичен POST
```


## API для пользователей

Просмотр активных опросов:

GET - api/availablequiz

Пример ответа:
```
[
    {
        "id": 18,
        "name": "First Quiz",
        "description": null
    },
    {
        "id": 19,
        "name": "Second Quiz",
        "description": null
    }
]
```

Просмотр вопросов активного опроса:

GET - api/answertoquiz/{id_активного _опроса}

Пример ответа:
```
{
    "questions": [
        {
            "id": 30,
            "name": "Which prefer?",
            "type": {
                "id": 6,
                "type": "ответ с выбором нескольких вариантов"
            },
            "question_option": [
                {
                    "id": 1,
                    "name": "Gitar"
                },
                {
                    "id": 2,
                    "name": "Piano"
                },
                {
                    "id": 4,
                    "name": "Bas"
                }
            ]
        },
        {
            "id": 32,
            "name": "Surname?",
            "type": {
                "id": 6,
                "type": "ответ с выбором нескольких вариантов"
            },
            "question_option": [
                {
                    "id": 18,
                    "name": "Ivanov"
                }
            ]
        }
    ]
}
```

Прохождение опроса:

POST - api/answertoquiz/{id_активного_опроса}


```
{
    "user_id": 123,                       // Обязательное поле. Принимает целое число. Если такого пользователя нет, то создает его 
    "answers": [                          // Принимает список объектов
        {
            "question": 22,
            "answer": "Dmitriy"
        },
        {
            "question": 23,
            "answer": "Kozlov"
        },
        {
            "question": 30,
            "answer": "Gitar"
        }
    ]
}
```

Просмотр пройденых опросов с детализацией:

GET - api/passedquiz/{user_id}

Пример ответа:
```
[
    {
        "id": 19,
        "name": "Second Quiz",
        "answers": [
            {
                "answer": "Gitar",
                "question": 30
            }
        ]
    }
]
```

> Добавлены всевозможные обработки ошибок
