# Лабораторная работа №3, вариант 7, средняя сложность №9
# Тема: класс для работы с файлами

import os


class FileManager:
    """Обёртка над файловыми операциями: запись, чтение, добавление, удаление."""

    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return f"FileManager({self.path!r})"

    # --- запись ---

    def write(self, text: str) -> None:
        """Перезаписать файл целиком."""
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(text)

    def append(self, text: str) -> None:
        """Добавить текст в конец файла."""
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(text)

    # --- чтение ---

    def read(self) -> str:
        """Прочитать файл целиком. Если файла нет — вернуть пустую строку."""
        if not self.exists():
            return ""
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def read_lines(self) -> list:
        """Прочитать файл как список строк без символов перевода строки."""
        if not self.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            return [line.rstrip("\n") for line in f]

    # --- служебное ---

    def exists(self) -> bool:
        return os.path.isfile(self.path)

    def clear(self) -> None:
        """Очистить содержимое файла, не удаляя сам файл."""
        self.write("")

    def delete(self) -> bool:
        """Удалить файл. Возвращает True, если файл был и удалён."""
        if self.exists():
            os.remove(self.path)
            return True
        return False

    # --- контекстный менеджер ---

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Здесь можно было бы закрывать соединение, если бы класс его держал.
        # У нас файл открывается и закрывается внутри каждого метода.
        return False  # не подавляем исключения


if __name__ == "__main__":
    path = "demo_file.txt"
    fm = FileManager(path)

    # Чистим возможные следы прошлых запусков
    fm.delete()

    print("fm =", fm)
    print("exists до записи:", fm.exists())
    assert fm.exists() is False

    fm.write("Первая строка\n")
    fm.append("Вторая строка\n")
    fm.append("Третья строка\n")

    print("exists после записи:", fm.exists())
    assert fm.exists() is True

    content = fm.read()
    print("--- содержимое ---")
    print(content, end="")
    assert content == "Первая строка\nВторая строка\nТретья строка\n"

    lines = fm.read_lines()
    print("read_lines:", lines)
    assert lines == ["Первая строка", "Вторая строка", "Третья строка"]

    fm.clear()
    assert fm.read() == ""
    print("после clear файл пуст, но существует:", fm.exists())

    fm.write("данные")
    deleted = fm.delete()
    print("delete вернул:", deleted, "| exists:", fm.exists())
    assert deleted is True and fm.exists() is False

    # Повторное удаление — False, исключения нет
    assert fm.delete() is False

    # Пример работы как контекстного менеджера
    with FileManager(path) as ctx_fm:
        ctx_fm.write("через with")
    assert FileManager(path).read() == "через with"
    FileManager(path).delete()

    print("Все проверки пройдены.")
