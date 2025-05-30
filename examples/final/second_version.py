import csv
import logging
import timeit

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def read_data(filename):
    data = []
    skip = 0
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                num = float(row[0])
                data.append(num)
            except (ValueError, IndexError):
                skip += 1
    logging.info("Пропущено %d строк", skip)
    return data

def calculate_mean(data):
    total = 0
    for num in data:
        total += num
    mean = total / len(data)
    return mean

def calculate_median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]
    return median

def calculate_std_dev(data):
    mean = calculate_mean(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    return std_dev

def write_results(filename, mean, median, std_dev):
    with open(filename, "w") as file:
        file.write(f"Среднее: {mean}\n")
        file.write(f"Медиана: {median}\n")
        file.write(f"Стандартное отклонение: {std_dev}\n")

def main():
    logging.info("Начало обработки файла")
    data = read_data("data.csv")
    if data:
        mean = calculate_mean(data)
        median = calculate_median(data)
        std_dev = calculate_std_dev(data)
        write_results("results.txt", mean, median, std_dev)
    else:
        logging.warning("Файл пуст или не содержит числовых данных")
        write_results("results.txt", 0, 0, 0)
    logging.info("Обработка завершена")

if __name__ == "__main__":
    logging.info(timeit.timeit(main, number=1))
