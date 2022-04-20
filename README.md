# Foodgram - сайт с рецептами
Foodgram (учебный проект Яндекс.Практикум) - сервис для публикации рецептов. Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачать список покупок.
Неавторизованным пользователям доступна регистрация, авторизация, просмотр рецептов других авторов.

## Подготовка и запуск проекта
### Установите docker на сервер:
```
sudo apt install docker.io 
```
### Установите docker-compose на сервер:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
### Отредактируйте файл infra/nginx.conf -> в строке server_name впишите IP сайта
### Склонировать репозиторий на сервер:
```
git@github.com:Hash466/foodgram-project-react.git
```
### Создайте файл .env и заполните переменные окружения
```
SECRET_KEY=<секретный ключ проекта django>

DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
POSTGRES_PASSWORD=<пароль для базы данных> - обязательный параметр
DB_NAME=<название базы данных> - необязательный параметр (по умолчанию будет postgres)
POSTGRES_USER=<имя пользователя> - необязательный параметр (по умолчанию будет postgres)

```

### Запустите docker-compose:
```
sudo docker-compose up -d --build
```
### После успешной сборки на сервере выполните команды (после первого деплоя):
#### Соберите статические файлы:
```
sudo docker-compose exec back python manage.py collectstatic --noinput
```
#### Применитe миграции:
```
sudo docker-compose exec backend python manage.py migrate --noinput
```
#### Загрузите ингридиенты в базу данных (не обязательно)
```
sudo docker-compose exec backend python manage.py loaddata fixtures/ingredients.json
```
#### Создать суперпользователя Django:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
### Проект будет доступен по вашему IP или домену
