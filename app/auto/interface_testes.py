from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, name):
        self.name = name

    def walk(self):
        print(f'{self.name} is walking')

class Talking(ABC):
    @abstractmethod
    def talk(self):
        ...


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def wag_tail(self):
        print(f'{self.name} is wagging tail')


class TalkingDog(Dog, Talking):
    def __init__(self, name):
        super().__init__(name)

    def talk(self):
        print(f'{self.name} says Hello.')





if __name__ == '__main__':
    pluto = Dog('Pluto')
    pluto.walk()
    pluto.wag_tail()

    goofy = TalkingDog('Goofy')
    goofy.walk()
    goofy.wag_tail()
    goofy.talk()