# Лабораторная работа №3, вариант 7, повышенная сложность №5
# Тема: класс для сериализации объектов в JSON

import json
from datetime import datetime, date


class JsonSerializer:
    """Сериализация Python-объектов в JSON и обратно.

    Поддерживает базовые типы, списки, словари, datetime/date
    и доменные объекты с методом to_dict().
    """

    @classmethod
    def dumps(cls, obj, indent=None) -> str:
        return json.dumps(
            obj,
            default=cls._default,
            ensure_ascii=False,
            indent=indent,
            sort_keys=True,
        )

    @classmethod
    def loads(cls, text: str):
        return json.loads(text, object_hook=cls._object_hook)

    @staticmethod
    def _default(o):
        # datetime и date — со служебной обёрткой, чтобы восстановить тип при loads
        if isinstance(o, datetime):
            return {"__type__": "datetime", "value": o.isoformat()}
        if isinstance(o, date):
            return {"__type__": "date", "value": o.isoformat()}
        # доменные объекты с to_dict()
        to_dict = getattr(o, "to_dict", None)
        if callable(to_dict):
            return {"__type__": type(o).__name__, "value": to_dict()}
        raise TypeError(f"Объект типа {type(o).__name__} не сериализуется в JSON")

    @staticmethod
    def _object_hook(d):
        t = d.get("__type__")
        if t == "datetime":
            return datetime.fromisoformat(d["value"])
        if t == "date":
            return date.fromisoformat(d["value"])
        return d


class Person:
    """Пример доменного класса с поддержкой JSON."""

    def __init__(self, name: str, age: int, birth=None):
        self.name = name
        self.age = age
        self.birth = birth  # datetime | date | None

    def to_dict(self) -> dict:
        return {"name": self.name, "age": self.age, "birth": self.birth}

    @classmethod
    def from_dict(cls, d: dict) -> "Person":
        return cls(name=d["name"], age=d["age"], birth=d.get("birth"))

    def to_json(self, indent=None) -> str:
        return JsonSerializer.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, text: str) -> "Person":
        return cls.from_dict(JsonSerializer.loads(text))

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return (self.name, self.age, self.birth) == (other.name, other.age, other.birth)

    def __repr__(self):
        return f"Person({self.name!r}, {self.age}, {self.birth!r})"


if __name__ == "__main__":
    # 1. Round-trip одного объекта с datetime
    p1 = Person("Анна", 22, datetime(2003, 5, 17, 14, 30))
    text = p1.to_json(indent=2)
    print("JSON одного объекта:")
    print(text)

    p1_back = Person.from_json(text)
    print("Восстановлено:", p1_back)
    assert p1_back == p1, "round-trip Person не совпал"
    assert isinstance(p1_back.birth, datetime)

    print()

    # 2. Прямая сериализация доменного объекта через JsonSerializer.dumps
    p2 = Person("Борис", 25, date(2000, 1, 1))
    text2 = JsonSerializer.dumps(p2)
    print("dumps(Person) напрямую:")
    print(text2)

    data = JsonSerializer.loads(text2)
    # Person в object_hook не зарегистрирован, поэтому достаём вручную
    p2_back = Person.from_dict(data["value"])
    assert p2_back == p2, "round-trip Person (через __type__) не совпал"
    assert isinstance(p2_back.birth, date)

    print()

    # 3. Смешанная вложенная структура
    people = [
        Person("Анна", 22, datetime(2003, 5, 17)),
        Person("Борис", 25, date(2000, 1, 1)),
        Person("Вера", 22, None),
    ]
    payload = {
        "generated_at": datetime(2026, 9, 1, 12, 0, 0),
        "people": people,
        "count": len(people),
        "tags": ["учебное", "json", "мини-проект"],
    }
    blob = JsonSerializer.dumps(payload, indent=2)
    print("Смешанная структура:")
    print(blob)

    restored = JsonSerializer.loads(blob)
    assert restored["count"] == 3
    assert isinstance(restored["generated_at"], datetime)
    assert restored["tags"] == ["учебное", "json", "мини-проект"]

    # восстановим Person-ов из их обёрток __type__
    restored_people = [Person.from_dict(x["value"]) for x in restored["people"]]
    assert restored_people == people, "список Person не восстановился"

    print()

    # 4. Ошибка на несериализуемом объекте
    try:
        JsonSerializer.dumps({"bad": {1, 2, 3}})  # set не поддерживается
    except TypeError as e:
        print("Ожидаемая ошибка:", e)

    print()
    print("Все проверки пройдены.")
