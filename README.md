# test_uow_structure

### Добавить .env файл со следующими параметрами:

```
POSTGRES_PASSWORD=ваш пароль
POSTGRES_USER=ваш пользователь
POSTGRES_DB=ваша бд
POSTGRES_HOST=db если запускаете в контейнере

APP_NAME=Customers

```

### Запустить контейнеры

```

docker-compose up -d --build

```

### Документация OpenAPI доступна по адресу: 

127.0.0.1:8000/docs


### Пример тестового JSON: 

```
{
  "first_name": "clark",
  "last_name": "kent",
  "orders": [
    {
      "price": 100,
      "name": "coat"
    },
   {
      "price": 100,
      "name": "shoes"
    }
  ]
}

```

