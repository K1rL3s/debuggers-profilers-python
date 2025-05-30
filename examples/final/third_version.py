import logging
import timeit
from functools import partial

import pandas as pd
from pandas import Series

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_csv(input_file, output_file):
    logging.info(f'Чтение файла {input_file}')
    df: pd.DataFrame = pd.read_csv(input_file, header=None, names=['value'], on_bad_lines='skip')
    numbers: Series = df['value'].dropna()

    if numbers.empty:
        logging.warning("Файл пуст или не содержит числовых данных")
        with open(output_file, 'w') as f:
            f.write("Среднее: 0\nМедиана: 0\nСтандартное отклонение: 0\n")
        return

    logging.info(f'Обработано {len(numbers):_} чисел')
    mean: float = numbers.mean()
    median: float = numbers.median()
    std_dev: float = numbers.std()

    logging.info('Вычисление завершено, запись результатов')
    with open(output_file, 'w') as f:
        f.write(f"Среднее: {mean}\nМедиана: {median}\nСтандартное отклонение: {std_dev}\n")
    logging.info(f'Результаты записаны в {output_file}')

if __name__ == "__main__":
    logging.info(
        timeit.timeit(
            partial(process_csv, "data.csv", "results.txt"),
            number=1
        )
    )
