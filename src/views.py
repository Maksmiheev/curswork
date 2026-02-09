import json
import datetime
import pandas as pd
import requests
from src.config import logger


def fetch_data_from_api(date_time_str):
    # Преобразование строки в объект datetime
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Формирование запроса к API
    api_url = f'http://api.example.com/data?timestamp={date_time_obj.timestamp()}'

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Ошибка при получении данных от API: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return None


def process_data(data):
    df = pd.DataFrame(data)
    processed_data = df.to_dict(orient='records')
    return processed_data


def generate_json_response(processed_data):
    return json.dumps(processed_data, ensure_ascii=False, indent=4)
