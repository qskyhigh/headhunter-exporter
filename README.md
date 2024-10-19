# HeadHunter Exporter

## Описание проекта

HeadHunter Exporter - это Python-приложение для сбора данных о вакансиях с сайта HeadHunter.ru через их API. Приложение позволяет собирать информацию о вакансиях, обрабатывать ее и сохранять в различных форматах, включая Google Sheets, PostgreSQL и SQLite.

## Основные функции

- Аутентификация через API HeadHunter
- Сбор данных о вакансиях с учетом различных параметров (профессиональные роли, опыт работы, регионы)
- Обработка и очистка полученных данных
- Сохранение данных в Google Sheets
- Сохранение данных в PostgreSQL
- Сохранение данных в SQLite

## Требования

- Python 3.7+
- pip (менеджер пакетов Python)

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/your-username/headhunter-exporter.git
   cd headhunter-exporter
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корневой директории проекта и добавьте необходимые переменные окружения:
   ```
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ACCESS_TOKEN=your_access_token
   REDIRECT_URI=your_redirect_uri
   
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   DB_DATABASE=your_db_name
   DB_SCHEMA=your_db_schema
   DB_TABLE=your_db_table
   
   GOOGLE_SHEET_PAGE_NAME=your_sheet_name
   ```

## Использование

1. Настройте параметры сбора данных в файле `config.py`.

2. Запустите основной скрипт:
   ```
   python main.py
   ```

3. Данные будут собраны и сохранены в соответствии с настройками в `config.py`.

## Структура проекта

- `main.py`: Основной скрипт для запуска сбора данных
- `modules/headhunter.py`: Модуль для работы с API HeadHunter
- `modules/google_sheets.py`: Модуль для работы с Google Sheets
- `modules/(sqlite/postgresql).py`: Модули для работы с базами данных (PostgreSQL и SQLite)
- `config.py`: Файл для загрузки конфигурации
- `config.yml`: Файл конфигурации
- `requirements.txt`: Список зависимостей проекта

## Настройка

Перед использованием убедитесь, что вы настроили следующее:

1. Получили необходимые учетные данные для API HeadHunter и добавили их в `.env` файл
2. Настроили доступ к Google Sheets API и добавили путь к файлу учетных данных в `config.yml`
3. Настроили параметры подключения к базам данных в `config.yml`
4. Выбрали целевой источник для сохранения данных в `config.yml` (sheets/postgres/sqlite)

## Конфигурация

Основные настройки проекта находятся в файле `config.yml`. В `config.py` эти настройки загружаются и преобразуются в переменные Python. Основные переменные конфигурации:

- `HH_AUTH_CODE`: Код авторизации HeadHunter (получается вручную)
- `HH_CLIENT_ID`, `HH_CLIENT_SECRET`, `HH_REDIRECT_URI`: Данные для аутентификации в API HeadHunter
- `HH_AREAS_URL`, `HH_VACANCIES_URL`: URL для API запросов
- `HH_EXPERIENCE_IDS`: Список ID опыта работы для фильтрации вакансий
- `HH_CATEGORY_ID`: Категория
- `HH_ROLES`: Список ID ролей, которые нужно искать
- `DB_SQLITE_PATH`: Путь к файлу SQLite базы данных
- `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_SCHEMA`, `DB_TABLE`: Настройки для PostgreSQL
- `GOOGLE_SHEETS_CONFIG_FILE`, `GOOGLE_SHEET_URL`, `GOOGLE_SHEET_PAGE_NAME`: Настройки для Google Sheets
- `TARGET_SOURCE`: Целевой источник для сохранения данных (sheets/postgres/sqlite)

Вы можете изменить эти параметры в `config.yml` для настройки работы приложения.
## Вклад в проект

Если вы хотите внести свой вклад в проект, пожалуйста, создайте issue или отправьте pull request.
