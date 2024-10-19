import requests
import json
import pandas as pd
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import itertools
from loguru import logger
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta


class HeadHunterAPI:
    def __init__(self, client_id: str, client_secret: str, access_token: str,
                 areas_url: str, vacancies_url: str, prof_id: List[int], exp_id: List[str]):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.areas_url = areas_url
        self.vacancies_url = vacancies_url
        self.prof_id = prof_id
        self.exp_id = exp_id

    def get_token(self, auth_code: str, redirect_uri: str) -> Optional[Dict[str, str]]:
        url = "https://hh.ru/oauth/token"
        body = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': redirect_uri
        }

        try:
            response = requests.post(url, data=body)
            response.raise_for_status()
            tokens = response.json()

            required_keys = ['access_token', 'token_type', 'refresh_token', 'expires_in']
            if not all(key in tokens for key in required_keys):
                logger.error("Response does not contain all required token data")
                return None

            Path("data").mkdir(parents=True, exist_ok=True)
            with open('data/token.json', 'w', encoding='utf-8') as f:
                json.dump(tokens, f, ensure_ascii=False, indent=4)

            logger.info("Token successfully retrieved and saved to data/token.json")
            return tokens

        except requests.RequestException as e:
            logger.error(f"Error requesting token: {e}")
        except json.JSONDecodeError:
            logger.error("Error decoding JSON response")
        except IOError as e:
            logger.error(f"Error saving file: {e}")

        return None

    def get_areas(self) -> List[int]:
        logger.info("Fetching list of areas")
        response = requests.get(self.areas_url)
        response.raise_for_status()
        areas = response.json()
        logger.info("Retrieved {} areas", len(areas[0]['areas']))
        return [int(area['id']) for area in areas[0]['areas']]

    @staticmethod
    def extract_value(item: Any, *keys: Union[str, int]) -> Any:
        for key in keys:
            if isinstance(item, dict):
                item = item.get(key, {})
            elif isinstance(item, list) and isinstance(key, int):
                item = item[key] if len(item) > key else {}
            else:
                return None
            if item is None:
                return None
        return item if isinstance(item, (int, str, bool)) else None

    def get_vacancies_inter(self, vacancies: Dict[str, Any]) -> pd.DataFrame:
        return pd.DataFrame({
            'id': [item['id'] for item in vacancies['items']],
            'name': [item['name'] for item in vacancies['items']],
            'area_id': [self.extract_value(item, 'area', 'id') for item in vacancies['items']],
            'area_name': [self.extract_value(item, 'area', 'name') for item in vacancies['items']],
            'professional_roles_id': [self.extract_value(item, 'professional_roles', 0, 'id') for item in
                                      vacancies['items']],
            'professional_roles_name': [self.extract_value(item, 'professional_roles', 0, 'name') for item in
                                        vacancies['items']],
            'employer_id': [self.extract_value(item, 'employer', 'id') for item in vacancies['items']],
            'employer_name': [self.extract_value(item, 'employer', 'name') for item in vacancies['items']],
            'snippet_requirement': [self.extract_value(item, 'snippet', 'requirement') for item in vacancies['items']],
            'snippet_responsibility': [self.extract_value(item, 'snippet', 'responsibility') for item in
                                       vacancies['items']],
            'experience': [self.extract_value(item, 'experience', 'name') for item in vacancies['items']],
            'employment': [self.extract_value(item, 'employment', 'name') for item in vacancies['items']],
            'salary_from': [self.extract_value(item, 'salary', 'from') for item in vacancies['items']],
            'salary_to': [self.extract_value(item, 'salary', 'to') for item in vacancies['items']],
            'salary_currency': [self.extract_value(item, 'salary', 'currency') for item in vacancies['items']],
            'salary_gross': [self.extract_value(item, 'salary', 'gross') for item in vacancies['items']],
            'created_at': [item['created_at'] for item in vacancies['items']],
            'published_at': [item['published_at'] for item in vacancies['items']],
            'url': [item['alternate_url'] for item in vacancies['items']],
        })

    def get_vacancies_result(self, args: tuple) -> Optional[pd.DataFrame]:
        page, prof_id, area_id, exp_id = args + (None,) * (4 - len(args))
        headers = {'Authorization': f'Bearer {self.access_token}'}
        query_list = {'professional_role': prof_id, 'per_page': 100, 'page': page}

        if area_id:
            query_list['area'] = area_id
        if exp_id:
            query_list['experience'] = exp_id

        response = requests.get(self.vacancies_url, headers=headers, params=query_list)
        response.raise_for_status()
        vacancies = response.json()

        if not vacancies['items']:
            return None

        vacancies_df_inter = self.get_vacancies_inter(vacancies)
        sleep(2)
        return vacancies_df_inter

    def collect_vacancies(self) -> pd.DataFrame:
        logger.info("Starting to collect vacancies")
        areas_id = self.get_areas()

        params = (
                list(itertools.product(range(20), [id for id in self.prof_id if id in [156, 165, 36, 104, 112, 114, 125]])) +
                list(itertools.product(range(20), [id for id in self.prof_id if id not in [156, 165, 36, 104, 112, 114, 125]], [1], self.exp_id)) +
                list(itertools.product(range(20),[id for id in self.prof_id if id not in [156, 165, 36, 104, 112, 114, 125]], [id for id in areas_id if id == 2]))
        )

        start_time = time()
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(self.get_vacancies_result, params))

        df = pd.concat([df.dropna(how='all', axis=1) for df in results if df is not None], ignore_index=True)
        logger.info("Vacancy collection completed in {:.2f} seconds", time() - start_time)
        return df

    @staticmethod
    def prepare_dataframe(df: pd.DataFrame, target_source: str) -> pd.DataFrame:
        logger.info("Preparing DataFrame")
        numeric_columns = ['id', 'area_id', 'professional_roles_id', 'employer_id', 'salary_from', 'salary_to']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(-1).astype('Int64')

        df['salary_gross'] = df['salary_gross'].astype(bool)

        date_columns = ['created_at', 'published_at']
        if target_source == 'sheets':
            df[date_columns] = df[date_columns].astype(str)
        else:
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.date

        logger.info("DataFrame prepared")
        return df

    @staticmethod
    def is_token_valid(file_path: str, max_age_days: int = 14) -> bool:
        if not Path(file_path).exists():
            logger.warning("Token file does not exist.")
            return False

        mod_time = Path(file_path).stat().st_mtime
        mod_date = datetime.fromtimestamp(mod_time)
        current_date = datetime.now()
        age = current_date - mod_date

        if age > timedelta(days=max_age_days):
            logger.warning(f"Token file is older than {max_age_days} days and might be expired.")
            return False

        logger.info(f"Token file is valid. Last modified: {mod_date}")
        return True
