from functools import reduce
import operator


class Item:
    def __init__(self, worry_level: int) -> None:
        self._worry_level = worry_level

    def __repr__(self) -> str:
        return f"Item_{self._worry_level}"
    
    @property
    def worry_level(self):
        return self._worry_level

    def inspection(self, operation: str, op_value: int = None):
        self._worry_level = self.operation_helper(
            base=self._worry_level,
            operation=operation,
            op_value=op_value
        )

    @staticmethod
    def operation_helper(base: int, operation: str, op_value: int = None) -> int | ValueError:
        if operation == "mul":
            return base * op_value
        elif operation == "add":
            return base + op_value
        elif operation == "power":
            return base * base

    @staticmethod
    def operation_helper_part1(
            base: int,
            operation: str,
            op_value: int = None, reduce_factor: int = 3
    ) -> int:
        if operation == "mul":
            return int((base * op_value) / reduce_factor)
        elif operation == "add":
            return int((base + op_value) / reduce_factor)
        elif operation == "power":
            return int((base * base) / reduce_factor)

    def factorize_worry_level(self, modulo_factor: int):
        self._worry_level %= modulo_factor


class Monkey:
    def __init__(
            self,
            monkey_id: int,
            start_items: list[Item],
            modulo_factor: int,
            tf_factor: tuple,
            operation: str,
            op_value: int = None
            ) -> None:
        self.monkey_id = monkey_id
        self._items = start_items
        self.modulo_factor = modulo_factor
        self.tf_factor = tf_factor
        self._counter = 0
        self._operation = operation
        self._op_value = op_value

    def __repr__(self) -> str:
        return f"Monkey_{self.monkey_id}"

    @property
    def counter(self):
        return self._counter

    @property
    def items(self) -> list[Item]:
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items

    def operation(self):
        self._counter += len(self._items)
        for item in self._items:
            item.inspection(operation=self._operation, op_value=self._op_value)
    
    def throwing(self):
        true_items = [item for item in self.items if item.worry_level % self.modulo_factor == 0]
        false_items = [item for item in self.items if item.worry_level % self.modulo_factor != 0]
        return true_items, false_items


class Squad:
    def __init__(self, monkeys: list[Monkey]) -> None:
        self._monkeys = monkeys

    @classmethod
    def from_text(cls, text: list[str]):
        monkeys = []
        while len(text) >= 7:
            monkey_id = int(text[0].replace("Monkey ", "")[:-1])
            items = text[1].replace("Starting items: ", "").split(", ")
            start_items: list[Item] = [Item(int(element)) for element in items]
            modulo_factor = int(text[3].replace("Test: divisible by ", ""))
            whole_operation = text[2].replace("Operation: new = old ", "")
            if whole_operation[0] == "+":
                operation = "add"
                op_val = int(whole_operation.replace("+ ", ""))
            elif "old" in whole_operation:
                operation = "power"
                op_val = None
            else:
                operation = "mul"
                op_val = int(whole_operation.replace("* ", ""))

            throw_true = int(text[4].replace("If true: throw to monkey ", ""))
            throw_false = int(text[5].replace("If false: throw to monkey ", ""))
            monkeys.append(
                Monkey(
                    monkey_id=monkey_id,
                    start_items=start_items,
                    modulo_factor=modulo_factor,
                    tf_factor=(throw_true, throw_false),
                    operation=operation,
                    op_value=op_val
                )
            )

            text = text[7:]

        return cls(monkeys=monkeys)

    @property
    def reduction_factor(self):
        return reduce(operator.mul, [monkey.modulo_factor for monkey in self._monkeys])

    def round(self):
        for monkey in self._monkeys:
            for itm in monkey.items:
                itm.factorize_worry_level(modulo_factor=self.reduction_factor)

            monkey.operation()
            true_items, false_items = monkey.throwing()

            true_monkey = self._monkeys[monkey.tf_factor[0]]
            false_monkey = self._monkeys[monkey.tf_factor[1]]

            true_monkey.items += true_items
            false_monkey.items += false_items

            monkey.items = []

    def rock(self, number_of_rounds: int) -> None:
        for i in range(number_of_rounds):
            self.round()

        self.print_result()

    def print_result(self):
        for monkey in self._monkeys:
            print(f"Monkey {monkey.monkey_id}: {monkey.counter}")

    def get_sorted_result(self):
        return sorted([monkey.counter for monkey in self._monkeys])


if __name__ == "__main__":
    with open("data/monkeys.ini", "r") as f:
        data_text = f.readlines()
        data_text = [entry.strip() for entry in data_text]

    squad = Squad.from_text(data_text)

    squad.rock(10000)

    sorted_result = squad.get_sorted_result()
    print(f"{sorted_result[-1]} and {sorted_result[-2]} result: {sorted_result[-1] * sorted_result[-2]}")
