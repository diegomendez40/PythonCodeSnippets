from numpy import random
from Character import *

class Driver:

    def __init__(self, message_callback):
        self.characters = [ElderlyCivilian(1, 1), Warrior(1, 1), Veteran(1, 1)]
        self.message_callback = message_callback

    def startBattle(self):
        surv_idx = 0 # Survivor index
        nextEnemy_idx = 1 # Next enemy
        self.next_turn(surv_idx, nextEnemy_idx)

    def next_turn(self, survivor_idx, nextEnemy_idx):
        if (nextEnemy_idx < len(self.characters)):
            survivor = self.characters[survivor_idx]
            enemy = self.characters[nextEnemy_idx]
            self.message_callback(f"\n\nA fight starts between {survivor.description} {survivor.name} and {enemy.description} {enemy.name}\n\n")
            survivor.print(self.message_callback)
            enemy.print(self.message_callback)
            while (survivor.isAlive() and enemy.isAlive()):
                if (survivor.attack() > enemy.attack()):
                    self.message_callback(f"{enemy.name} gets hit")
                    enemy.health -= 1
                    enemy.print(self.message_callback)
                else:
                    self.message_callback(f"{survivor.name} gets hit")
                    survivor.health -=1
                    survivor.print(self.message_callback)
            if (survivor.isAlive()):
                survivor_idx = survivor_idx
            else:
                survivor_idx = nextEnemy_idx
            survivor = self.characters[survivor_idx]
            self.message_callback(f"This is the winning survivor: {survivor.description} {survivor.name}")
            survivor.print(self.message_callback)
            self.next_turn(survivor_idx, nextEnemy_idx+1)
        else:
            self.endBattle()

    def endBattle(self):
        self.message_callback("\n\nThe battle is over.")

            



