# Проект YaCut

## Описание проекта

Проект представляет собой сервис укорачивания ссылок с возможностью редиректа, по короткой ссылке, на оригинальную.

## Функционал проекта

Пользователь может сгенерировать короткую ссылку, сопоставляющуюся с оригинальной, как свою собственную, так и автоматически. После обращения к сервису, по короткой ссылке, пользователь будет перенаправлен по исходной ссылке.

## Инструкция по запуску проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/x9ilx/yacut.git
```

```
cd yacut
```
Для подготовки проекта к запуску необходимо создать вируальное окружение в директории проекта:

```bash
# windows
python -m venv venv

# linux
python3 -m venv venv
```

после чего активировать его и установить необходимые зависимости

```bash
# windows
source venv/scripts/activate
pip install -r requirements.txt

# linux
. bin/scripts/activate
pip install -r requirements.txt
```

Инициализировать бд и сделать миграции:

```bash
flask db migrate
```

Чтобы запустить приложение в режиме разработки необходимо выполнить команду:

```bash
flask run
```

База данных создастся автоматически. при запуске проекта (миграции применены не будут, в случае если были внесены изменения в модели, то необходимо выполнить миграции вручную)

## Иcпользованные технологии
- Python -  высокоуровневый язык программирования общего назначения с динамической строгой типизацией и автоматическим управлением памятью

- Flask - фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.

- SQLAlchemy - программная библиотека на языке Python для работы с реляционными СУБД с применением технологии ORM. Служит для синхронизации объектов Python и записей реляционной базы данных. SQLAlchemy позволяет описывать структуры баз данных и способы взаимодействия с ними на языке Python без использования SQL

- Alembic - это инструмент для миграции баз данных, написанный автором SQLAlchemy.

- WTForms - это гибкая библиотека для валидации и рендеринга форм для веб-разработки на Python. Она может работать с любым веб-фреймворком и шаблонизатором, которые вы выберете. Она поддерживает валидацию данных, защиту от CSRF, интернационализацию (I18N) и многое другое.


## Автор
[Бондаренко Владимир Викторович](https://github.com/x9ilx)