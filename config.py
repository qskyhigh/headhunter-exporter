import os
import json
import yaml
from pathlib import Path


def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Load main configuration
config = load_yaml_config('config.yml')

# Load additional JSON files
INDUSTRIES = load_json_file('data/industries.json')
ROLES = load_json_file('data/roles.json')
TOKEN = load_json_file('data/token.json')

# Google Sheets configuration
GOOGLE_SHEETS_CONFIG_FILE = config['google_sheets']['config_file']
GOOGLE_SHEET_URL = config['google_sheets']['sheet_url']
GOOGLE_SHEET_PAGE_NAME = config['google_sheets']['page_name']

# HeadHunter configuration
# TODO: Получать HH_AUTH_CODE автомататически, сейчас надо его получать вручную с api.hh.ru
HH_AUTH_CODE = config['headhunter']['auth_code']
HH_CLIENT_ID = config['headhunter']['client_id']
HH_CLIENT_SECRET = config['headhunter']['client_secret']
HH_REDIRECT_URI = config['headhunter']['redirect_uri']
HH_AREAS_URL = config['headhunter']['areas_url']
HH_VACANCIES_URL = config['headhunter']['vacancies_url']
HH_EXPERIENCE_IDS = config['headhunter']['experience_ids']
HH_NOT_INTERESTED_ROLES = config['headhunter']['not_interested_roles']
HH_ACCESS_TOKEN = TOKEN['access_token']

# Compute professional IDs
HH_PROF_ID = [
    int(role['id']) for category in ROLES['categories']
    if category['id'] == '11'
    for role in category['roles']
    if role['id'] not in HH_NOT_INTERESTED_ROLES
]

# Database configuration
# SQLite
DB_SQLITE_PATH = config['database']['sqlite']['path']

# PostgreSQL
DB_USERNAME = config['database']['postgres']['username']
DB_PASSWORD = config['database']['postgres']['password']
DB_HOST = config['database']['postgres']['host']
DB_PORT = config['database']['postgres']['port']
DB_DATABASE = config['database']['postgres']['database']
DB_SCHEMA = config['database']['postgres']['schema']
DB_TABLE = config['database']['postgres']['table']

# Target source
TARGET_SOURCE = config['target_source']
