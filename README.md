# HeadHunter Data Collector

## Описание проекта

HeadHunter Data Collector - это Python-приложение для сбора данных о вакансиях с сайта HeadHunter.ru через их API. Приложение позволяет собирать информацию о вакансиях, обрабатывать ее и сохранять в различных форматах, включая Google Sheets, PostgreSQL и SQLite.

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
   git clone https://github.com/your-username/headhunter-data-collector.git
   cd headhunter-data-collector
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
- `config.yml`: Файл конфигурации
- `requirements.txt`: Список зависимостей проекта

## Настройка

Перед использованием убедитесь, что вы настроили следующее:

1. Получили необходимые учетные данные для API HeadHunter
2. Настроили доступ к Google Sheets API (если планируете использовать эту функцию)
3. Настроили доступ к базе данных PostgreSQL (если планируете использовать эту функцию)

## Вклад в проект

Если вы хотите внести свой вклад в проект, пожалуйста, создайте issue или отправьте pull request.
