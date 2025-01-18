import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        """
        Ініціалізуємо фільтр Блума.

        :param size: Розмір бітового масиву.
        :param num_hashes: Кількість хеш-функцій.
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item: str):
        """
        Генеруємо набір хешів для заданого елемента.

        :param item: Елемент для хешування.
        :return: Генератор хеш-значень.
        """
        for i in range(self.num_hashes):
            yield mmh3.hash(item, i) % self.size

    def add(self, item: str):
        """
        Додаємо елемент до фільтра Блума.

        :param item: Елемент для додавання.
        """
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def check(self, item: str) -> bool:
        """
        Перевіряємо, чи є елемент у фільтрі Блума.

        :param item: Елемент для перевірки.
        :return: True, якщо елемент може бути у фільтрі, інакше False.
        """
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list) -> dict:
    """
    Перевіряє список паролів на унікальність.

    :param bloom_filter: Екземпляр BloomFilter.
    :param passwords: Список паролів для перевірки.
    :return: Словник з результатами перевірки.
    """
    results = {}

    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "Некоректний пароль"
        elif bloom_filter.check(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = [
        "password123",
        "newpassword",
        "admin123",
        "guest",
        "",
        None,
        " ",
    ]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
