## Описание
Веб приложение, которое позволяет загружать и парсить CSV-файл.
Файлы могут быть большими (несколько сотен мегабайт), поэтому обработка файлов реализована с помощью Celery и Redis.
Приложение должно отображать статус загрузки и обработки файла в режиме реального времени.

## Установка и запуск

1. Клонируйте этот репозиторий
2. Создайте в PostgreSQL базу данных categ (или сами укажите путь к своей БД в файле config.py) (не забудьте запустить сервер)
3. Создайте виртуальную среду и установите все зависимости с помощью `pip install -r requirements.txt`
5. Сделайте миграции c помощью Flask-Migrate:
`$ python app.py db init`
`$ python app.py db migrate`
`$ python app.py db upgrade`
6. Откройте второе окно терминала и запустите в нем локальный сервер Redis (`redis-server`)
7. Откройте третье окно терминала и запустите Celery 
`venv/bin/celery -A uploader.__init__.celery  worker --loglevel=info`
8. Запустите само приложение `venv/bin/python app.py`

## TODO:

1. Уделить больше внимания верстке и скриптам
2. После обновления страницы отображается только последний запущенный процесс, а не все.
3. Более разумная архитектура БД? Дерево категорий или хотя бы еще одна сущность для айди категорий?
4. Не использовать тяжеловесный Pandas для столь тривиальной задачи?