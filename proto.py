from typing import Protocol

class Animal(Protocol):
    def feed(self, data: int) -> None:
        pass

    # def eats(self) -> None:
    #     pass

class Duck:
    def feed(self) -> None:
        print("Duck eats")

def feed(animal: Animal) -> None:
    animal.feed()

duck = Duck()
feed(duck)

