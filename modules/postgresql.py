from loguru import logger
import psycopg2
from psycopg2 import sql


class PgDatabaseConnector:
    def __init__(self, dbname, dbschema, user, password, host, port, table):
        self.dbname = dbname
        self.dbschema = dbschema
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.table = table

    def __enter__(self):
        self.connection = self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def connect(self):
        return psycopg2.connect(dbname=self.dbname, user=self.user,
                                password=self.password, host=self.host, port=self.port)

    def save_to_database(self, df):
        logger.info("Saving data to the database")

        drop_table_query = sql.SQL(f"DROP TABLE IF EXISTS {self.dbschema}.{self.table};")
        with self.connection.cursor() as cursor:
            cursor.execute(drop_table_query)
            self.connection.commit()
        logger.info(f"Existing table {self.table} dropped")

        create_table_query = sql.SQL(f"""
            CREATE TABLE {self.dbschema}.{self.table} (
                id BIGINT NULL,
                name TEXT NULL,
                area_id BIGINT NULL,
                area_name TEXT NULL,
                professional_roles_id BIGINT NULL,
                professional_roles_name TEXT NULL,
                employer_id BIGINT NULL,
                employer_name TEXT NULL,
                snippet_requirement TEXT NULL,
                snippet_responsibility TEXT NULL,
                experience TEXT NULL,
                employment TEXT NULL,
                salary_from FLOAT8 NULL,
                salary_to FLOAT8 NULL,
                salary_currency TEXT NULL,
                salary_gross BOOLEAN NULL,
                created_at DATE NULL,
                published_at DATE NULL,
                url TEXT NULL
            );
        """)
        with self.connection.cursor() as cursor:
            cursor.execute(create_table_query)
            self.connection.commit()
        logger.info(f"Table {self.table} successfully created")

        df.to_sql(self.table, self.connection, schema=self.dbschema, if_exists='replace', index=False)

        create_index_sql = f"""
        CREATE INDEX IF NOT EXISTS ix_public_vacancies 
        ON {self.dbschema}.{self.table} 
        (published_at, name, area_name, professional_roles_name, employer_name);
        """
        with self.connection.cursor() as cursor:
            cursor.execute(create_index_sql)
            self.connection.commit()
        logger.info(f"Index on {self.table} successfully created")
