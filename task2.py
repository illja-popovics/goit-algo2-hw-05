import re
import time
from collections import Counter
from hyperloglog import HyperLogLog
import pandas as pd


def load_data(file_path):
    """
    Завантажує дані з лог-файлу, витягуючи IP-адреси.

    :param file_path: Шлях до лог-файлу.
    :return: Список IP-адрес.
    """
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    ips = []

    with open(file_path, "r") as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ips.append(match.group())

    return ips


def exact_unique_count(ips):
    """
    Точно підраховує кількість унікальних IP-адрес.

    :param ips: Список IP-адрес.
    :return: Кількість унікальних IP.
    """
    return len(set(ips))


def approximate_unique_count(ips):
    """
    Наближено підраховує кількість унікальних IP-адрес за допомогою HyperLogLog.

    :param ips: Список IP-адрес.
    :return: Оцінка кількості унікальних IP.
    """
    hll = HyperLogLog(0.01)  # 1% похибка
    for ip in ips:
        hll.add(ip)
    return len(hll)


def compare_methods(file_path):
    """
    Завантажує дані, рахує кількість унікальних IP точним та наближеним методом і порівнює їх.

    :param file_path: Шлях до лог-файлу.
    :return: Таблиця порівняння.
    """
    ips = load_data(file_path)

    # Точний підрахунок
    start_time = time.time()
    exact_count = exact_unique_count(ips)
    exact_time = time.time() - start_time

    # Наближений підрахунок
    start_time = time.time()
    approximate_count = approximate_unique_count(ips)
    approximate_time = time.time() - start_time

    # Створення таблиці результатів
    results = {
        "Метод": ["Точний підрахунок", "HyperLogLog"],
        "Унікальні елементи": [exact_count, approximate_count],
        "Час виконання (сек.)": [exact_time, approximate_time],
    }

    df_results = pd.DataFrame(results)
    return df_results


if __name__ == "__main__":
    # Шлях до файлу
    log_file_path = "lms-stage-access.log"

    # Порівняння методів
    comparison_results = compare_methods(log_file_path)

    # Виведення результатів
    print("Результати порівняння:")
    print(comparison_results)
