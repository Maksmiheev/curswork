from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


# Декоратор для записи результатов в файл
def report_writer(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename:
                file_path = filename
            else:
                file_path = f"{func.__name__}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            with open(file_path, "w") as file:
                file.write(result.to_string())
            return result

        return wrapper

    return decorator


# Функция для получения даты трех месяцев назад
def get_three_months_ago():
    now = datetime.now()
    three_months_ago = now.replace(day=1) - relativedelta(months=3)
    return three_months_ago



# Функция для получения траты по категории
@report_writer()
def spending_by_category(transactions: pd.DataFrame) -> pd.DataFrame:
    return (
        transactions.groupby("category")["amount"]
        .sum()
        .reset_index(name="total_amount")
    )


# Функция для получения средних трат по дням недели
@report_writer()
def spending_by_weekday(transactions: pd.DataFrame) -> pd.Series:
    return (
        transactions.groupby(transactions["date"].dt.weekday)["amount"]
        .mean()
        .rename_axis("weekday")
    )


# Функция для получения средних трат в рабочий и выходной день
@report_writer()
def spending_by_workday(transactions: pd.DataFrame) -> pd.Series:
    s = (
        transactions.assign(
            is_workday=transactions["date"].dt.weekday.isin([0, 1, 2, 3, 4])
        )
        .groupby("is_workday")["amount"]
        .mean()
    )
    s.index.name = "is_workday"  # Устанавливаем имя индекса одинаково
    return s
