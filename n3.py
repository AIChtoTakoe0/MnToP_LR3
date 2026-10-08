# Лабораторная работа №3, вариант 7, средняя сложность №3
# Тема: класс «Банковский счёт» с пополнением и снятием

class BankAccount:
    """Банковский счёт с операциями пополнения и снятия."""

    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.owner = owner
        self._balance = float(balance)
        self._history = []  # список кортежей (тип_операции, сумма, баланс_после)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        """Пополнить счёт. Возвращает новый баланс."""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self._balance += amount
        self._history.append(("deposit", amount, self._balance))
        return self._balance

    def withdraw(self, amount: float) -> float:
        """Снять со счёта. Возвращает новый баланс."""
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if amount > self._balance:
            raise ValueError(
                f"Недостаточно средств: на счёте {self._balance:.2f}, запрошено {amount:.2f}"
            )
        self._balance -= amount
        self._history.append(("withdraw", amount, self._balance))
        return self._balance

    def history(self):
        """Список выполненных операций."""
        return list(self._history)

    def __repr__(self):
        return f"BankAccount({self.owner!r}, balance={self._balance:.2f})"

    def __str__(self):
        return f"Счёт владельца «{self.owner}»: {self._balance:.2f} руб."


# ---------- интерактивная часть ----------

def ask_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Пустое значение. Попробуйте снова.")


def ask_float(prompt: str, default=None) -> float:
    """Число с плавающей точкой. Принимает и точку, и запятую. Пустой ввод → default."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("Нужно число. Попробуйте снова.")


def choose_menu() -> str:
    print()
    print("Операции:")
    print("  1 — пополнить счёт")
    print("  2 — снять со счёта")
    print("  3 — показать баланс")
    print("  4 — история операций")
    print("  0 — выход")
    return input("Ваш выбор: ").strip()


def main() -> None:
    print("=== Банковский счёт ===")
    owner = ask_nonempty("Имя владельца счёта: ")
    initial = ask_float("Начальный баланс [Enter = 0]: ", default=0.0)

    try:
        acc = BankAccount(owner, initial)
    except ValueError as e:
        print("Ошибка:", e)
        return

    print("Создан:", acc)

    while True:
        choice = choose_menu()

        if choice == "0":
            print("Завершение работы.")
            return

        if choice == "1":
            amount = ask_float("Сумма пополнения: ")
            try:
                new_balance = acc.deposit(amount)
                print(f"Пополнено на {amount:.2f}. Баланс: {new_balance:.2f}")
            except ValueError as e:
                print("Ошибка:", e)

        elif choice == "2":
            amount = ask_float("Сумма снятия: ")
            try:
                new_balance = acc.withdraw(amount)
                print(f"Снято {amount:.2f}. Баланс: {new_balance:.2f}")
            except ValueError as e:
                print("Ошибка:", e)

        elif choice == "3":
            print(acc)

        elif choice == "4":
            hist = acc.history()
            if not hist:
                print("Операций пока не было.")
            else:
                for i, (op, amount, bal) in enumerate(hist, 1):
                    name = "пополнение" if op == "deposit" else "снятие  "
                    print(f"{i}. {name}: {amount:+.2f} → баланс {bal:.2f}")

        else:
            print("Неизвестный пункт меню. Введите число от 0 до 4.")


if __name__ == "__main__":
    main()
