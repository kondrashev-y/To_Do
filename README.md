Репозиторий приложения Список задач (ToDO) на Django 3 и Django REST
Framework.

Установка (для пользователей операционных систем семейства **MacOs/Linux**):

1. Открыть терминал или консоль и перейти в нужную Вам директорию
2. Прописать команду `git clone https://github.com/kondrashev-y/To_Do`
3. Прописать следующие команды:
- `python3 -m venv venv`
- `source venv/bin/activate`
-  Перейти в директорию **Django-image** `cd To_Do/`
- `pip install -r requirements.txt`
- `python manage.py migrate`
4. Запустить сервер - `python manage.py runserver`
5. В браузере перейти по ссылке  http://127.0.0.1:8000/api/

Задачи реализованные в приложении: 
1. Создавать/редактировать/удалять задачу
2. Определять задаче крайний срок выполнения
3. Отмечать задачу выполненной
4. Поддержка меток (тегов)
5. Загружать данные по задачам из файлов (формат CSV)
6. Выгружать данные по задачам в файл на локальный компьютер (формат CSV)

Описание REST API приложения http://127.0.0.1:8000/swagger/?format=openapi