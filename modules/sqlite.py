from sqlalchemy import create_engine, Column, Integer, Float, Boolean, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from loguru import logger

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    area_id = Column(Integer)
    area_name = Column(Text)
    professional_roles_id = Column(Integer)
    professional_roles_name = Column(Text)
    employer_id = Column(Integer)
    employer_name = Column(Text)
    snippet_requirement = Column(Text)
    snippet_responsibility = Column(Text)
    experience = Column(Text)
    employment = Column(Text)
    salary_from = Column(Float)
    salary_to = Column(Float)
    salary_currency = Column(Text)
    salary_gross = Column(Boolean)
    created_at = Column(Date)
    published_at = Column(Date)
    url = Column(Text)


class SQLiteDatabaseConnector:
    def __init__(self, db_path):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database engine created")

    def __enter__(self):
        self.session = self.Session()
        logger.info("Database session started")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
        logger.info("Database session closed")

    def recreate_tables(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        logger.info("Tables dropped and recreated")

    def save_to_database(self, dataframe: pd.DataFrame):
        try:
            vacancies = [Vacancy(**row) for row in dataframe.to_dict(orient='records')]
            self.session.bulk_save_objects(vacancies)
            self.session.commit()
            logger.info(f"Inserted {len(vacancies)} records into the vacancies table")
        except Exception as e:
            self.session.rollback()
            logger.error("Error saving data to the database: {}", e)
            raise
