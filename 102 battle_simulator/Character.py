from numpy import random

class Character:

    def __init__(self, health, strength, name='NoName', description='Character'):
        self.health = health
        self.strength = strength
        self.description = description
        self.name = name

    def isAlive(self):
        return (self.health > 0)
    
    def attack(self):
        return (self.strength)

    def print(self, message_callback=None):
        message = f"{self.description} {self.name} has health {self.health} and strength {self.strength}."
        if message_callback:
            message_callback(message)
        else:
            print(message)

class ElderlyCivilian(Character):

    def __init__(self, health, strength, name='Elon', description='Elderly Civilian'):
        health = 1
        strength = random.randint(6)
        super().__init__(health, strength, name, description)

class Warrior(Character):

    def __init__(self, health, strength, name='Warren', description='Warrior'):
        health = 2
        strength = random.randint(9)
        super().__init__(health, strength, name, description)

class Veteran(Character):

    def __init__(self, health, strength, name='Viterbi', description='Veteran'):
        health = 3
        strength = random.randint(12)
        super().__init__(health, strength, name, description)