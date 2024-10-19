from loguru import logger
from config import (GOOGLE_SHEET_PAGE_NAME, TARGET_SOURCE, DB_SCHEMA, DB_TABLE, DB_SQLITE_PATH, HH_REDIRECT_URI,
                    HH_AUTH_CODE, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE, HH_CLIENT_ID,
                    HH_CLIENT_SECRET, HH_ACCESS_TOKEN, HH_AREAS_URL, HH_VACANCIES_URL, HH_PROF_ID, HH_EXPERIENCE_IDS)
from modules import *

TOKEN_FILE_PATH = 'data/token.json'


def setup_hh_api():
    hh_api = HeadHunterAPI(HH_CLIENT_ID, HH_CLIENT_SECRET, HH_ACCESS_TOKEN, HH_AREAS_URL, HH_VACANCIES_URL, HH_PROF_ID,
                           HH_EXPERIENCE_IDS)
    if not hh_api.is_token_valid(TOKEN_FILE_PATH):
        logger.info("Requesting new token")
        token = hh_api.get_token(HH_AUTH_CODE, HH_REDIRECT_URI)
        if token:
            logger.info("New token successfully retrieved and saved")
        else:
            logger.error("Failed to retrieve new token")
            raise Exception("Token retrieval failed")
    else:
        logger.info("Token is valid")
    return hh_api


def collect_and_prepare_data(hh_api):
    logger.info("Starting data collection process")
    vacancies_df = hh_api.collect_vacancies()
    vacancies_df = vacancies_df.drop_duplicates(subset='id')
    return hh_api.prepare_dataframe(vacancies_df, TARGET_SOURCE)


def save_to_sheets(df):
    google_sheets = GoogleSheets(GOOGLE_SHEET_PAGE_NAME)
    google_sheets.update_worksheet(df)
    logger.info("Data successfully saved to Google Sheets")


def save_to_postgres(df):
    with PgDatabaseConnector(dbname=DB_DATABASE, dbschema=DB_SCHEMA, user=DB_USERNAME,
                             password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, table=DB_TABLE) as db:
        db.save_to_database(df)
        logger.info("Data successfully saved to PostgreSQL database")


def save_to_sqlite(df):
    with SQLiteDatabaseConnector(DB_SQLITE_PATH) as db:
        db.recreate_tables()
        db.save_to_database(df)
        logger.info("Data successfully saved to SQLite database")


def main():
    try:
        hh_api = setup_hh_api()
        vacancies_df = collect_and_prepare_data(hh_api)

        if TARGET_SOURCE == 'sheets':
            save_to_sheets(vacancies_df)
        elif TARGET_SOURCE == 'postgres':
            save_to_postgres(vacancies_df)
        elif TARGET_SOURCE == 'sqlite':
            save_to_sqlite(vacancies_df)
        else:
            logger.error(f"Unsupported TARGET_SOURCE: {TARGET_SOURCE}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
