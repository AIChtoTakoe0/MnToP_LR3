# task_medium_7.py
# Лабораторная работа №3, вариант 7, средняя сложность №7
# Тема: перегрузка оператора +

class Vector:
    """Двумерный вектор с поддержкой операции +."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        # Vector + Vector
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        # Vector + число: прибавляем число к обеим координатам
        if isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        # Не знаем, как складывать — пусть Python попробует other.__radd__
        return NotImplemented

    def __radd__(self, other):
        # Поддержка выражений вида 5 + vector
        return self.__add__(other)

    def __eq__(self, other):
        # Удобно для проверок в тестах и примерах
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented


if __name__ == "__main__":
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    print("v1 =", v1)
    print("v2 =", v2)

    v3 = v1 + v2
    print("v1 + v2 =", v3)
    assert v3 == Vector(4, 6), "Ошибка: Vector + Vector"

    v4 = v1 + 10
    print("v1 + 10 =", v4)
    assert v4 == Vector(11, 12), "Ошибка: Vector + число"

    v5 = 10 + v1
    print("10 + v1 =", v5)
    assert v5 == Vector(11, 12), "Ошибка: число + Vector (через __radd__)"

    try:
        v1 + "строка"
    except TypeError as e:
        print("Ожидаемая ошибка при v1 + 'строка':", e)

    print("Все проверки пройдены.")
