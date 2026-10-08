# Лабораторная работа №3, вариант 7, повышенная сложность №7
# Тема: мини-ORM — класс «Таблица», методы insert, select

class Table:
    """Мини-ORM: таблица в памяти с колонками и строками-словарями."""

    def __init__(self, name: str, columns):
        if not name:
            raise ValueError("Имя таблицы не может быть пустым")
        columns = list(columns)
        if not columns:
            raise ValueError("У таблицы должна быть хотя бы одна колонка")
        if len(columns) != len(set(columns)):
            raise ValueError("Имена колонок не должны повторяться")

        self.name = name
        self.columns = columns
        self._rows = []

    # ---------- вставка ----------

    def insert(self, **kwargs) -> dict:
        """Вставить строку. Возвращает вставленный словарь."""
        missing = [c for c in self.columns if c not in kwargs]
        if missing:
            raise ValueError(f"Отсутствуют обязательные колонки: {missing}")

        extra = [k for k in kwargs if k not in self.columns]
        if extra:
            raise ValueError(f"Неизвестные колонки: {extra}")

        row = {c: kwargs[c] for c in self.columns}
        self._rows.append(row)
        return row

    # ---------- выборка ----------

    def select(self, **conditions):
        """Вернуть строки, у которых все указанные колонки равны значениям."""
        unknown = [k for k in conditions if k not in self.columns]
        if unknown:
            raise ValueError(f"Условие по неизвестным колонкам: {unknown}")

        result = []
        for row in self._rows:
            if all(row[c] == v for c, v in conditions.items()):
                # отдаём копию, чтобы снаружи нельзя было изменить внутреннее состояние
                result.append(dict(row))
        return result

    # ---------- дополнительные операции ----------

    def delete(self, **conditions) -> int:
        """Удалить строки по условиям. Возвращает количество удалённых."""
        unknown = [k for k in conditions if k not in self.columns]
        if unknown:
            raise ValueError(f"Условие по неизвестным колонкам: {unknown}")

        before = len(self._rows)
        self._rows = [
            row for row in self._rows
            if not all(row[c] == v for c, v in conditions.items())
        ]
        return before - len(self._rows)

    def count(self) -> int:
        return len(self._rows)

    def all(self):
        return [dict(row) for row in self._rows]

    # ---------- представление ----------

    def __repr__(self):
        return f"Table(name={self.name!r}, columns={self.columns}, rows={self.count()})"

    def __str__(self):
        header = " | ".join(self.columns)
        sep = "-" * len(header)
        lines = [f"Таблица «{self.name}»", header, sep]
        for row in self._rows:
            lines.append(" | ".join(str(row[c]) for c in self.columns))
        if not self._rows:
            lines.append("(пусто)")
        return "\n".join(lines)


# ---------- демонстрация ----------

if __name__ == "__main__":
    users = Table("users", ["id", "name", "age"])

    # insert
    users.insert(id=1, name="Анна", age=22)
    users.insert(id=2, name="Борис", age=25)
    users.insert(id=3, name="Вера", age=22)
    users.insert(id=4, name="Глеб", age=30)

    print(users)
    print()

    # select без условий — все строки
    all_rows = users.select()
    print("select() →", all_rows)
    assert len(all_rows) == 4

    # select с одним условием
    age22 = users.select(age=22)
    print("select(age=22) →", age22)
    assert len(age22) == 2
    assert {r["name"] for r in age22} == {"Анна", "Вера"}

    # select с двумя условиями (AND)
    anna = users.select(name="Анна", age=22)
    print("select(name='Анна', age=22) →", anna)
    assert anna == [{"id": 1, "name": "Анна", "age": 22}]

    # пустая выборка
    nobody = users.select(name="Никто")
    print("select(name='Никто') →", nobody)
    assert nobody == []

    # ошибки валидации
    try:
        users.insert(id=5, name="Дмитрий")  # нет age
    except ValueError as e:
        print("Ожидаемая ошибка insert:", e)

    try:
        users.insert(id=6, name="Егор", age=19, city="Москва")  # лишняя колонка
    except ValueError as e:
        print("Ожидаемая ошибка insert:", e)

    try:
        users.select(city="Москва")
    except ValueError as e:
        print("Ожидаемая ошибка select:", e)

    # delete и count
    removed = users.delete(age=22)
    print(f"delete(age=22) удалил {removed} строк(и)")
    assert removed == 2
    assert users.count() == 2
    print()
    print(users)

    # select после delete
    remaining = users.select()
    assert {r["name"] for r in remaining} == {"Борис", "Глеб"}

    print()
    print("Все проверки пройдены.")
