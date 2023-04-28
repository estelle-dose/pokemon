import json
import random

class Pokemon:
    def __init__(self, name, hp, level, attack_power, defense, type):
        self._name = name
        self._hp = hp
        self.level = level
        self.attack_power = attack_power
        self.defense = defense
        self.type = type

    def get_name(self):
        return self._name

    def get_hp(self):
        return self._hp

    def set_hp(self, new_hp):
        self._hp = new_hp

class Normal(Pokemon):
    def __init__(self, name, hp, level, attack_power, defense):
        super().__init__(name, hp, level, attack_power, defense, "Normal")
        self._hp *= 1.2
        self.attack_power *= 0.9

class Feu(Pokemon):
    def __init__(self, name, hp, level, attack_power, defense):
        super().__init__(name, hp, level, attack_power, defense, "Feu")
        self.attack_power *= 1.2
        self.defense *= 0.8

class Eau(Pokemon):
    def __init__(self, name, hp, level, attack_power, defense):
        super().__init__(name, hp, level, attack_power, defense, "Eau")
        self.defense *= 1.2

class Terre(Pokemon):
    def __init__(self, name, hp, level, attack_power, defense):
        super().__init__(name, hp, level, attack_power, defense, "Terre")
        self.attack_power *= 1.1
        self.defense *= 1.1

evoli = Normal("Evoli", 100, 5, 10, 5)
salameche = Feu("Salameche", 80, 5, 8, 6)
carapuce = Eau("Carapuce", 90, 5, 7, 7)
bulbizarre = Terre("Bulbizarre", 110, 5, 9, 8)

class Combat:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2

    def is_alive(self, pokemon):
        return pokemon.get_hp() > 0

    def get_winner(self):
        if self.is_alive(self.pokemon1) and self.is_alive(self.pokemon2):
            return None
        elif self.is_alive(self.pokemon1):
            return self.pokemon1
        else:
            return self.pokemon2

    def can_attack(self, pokemon):
        return random.random() <= 0.8

    def get_opponent_type(self, pokemon):
        if pokemon == self.pokemon1:
            return self.pokemon2.type
        else:
            return self.pokemon1.type

    def record_pokedex(self, pokemon):
        with open("pokedex.json", "r+") as f:
            pokedex = json.load(f)
            pokedex.append({
                "name": pokemon.get_name(),
                "hp": pokemon.get_hp(),
                "level": pokemon.level,
                "attack_power": pokemon.attack_power,
                "defense": pokemon.defense,
                "type": pokemon.type
            })
            f.seek(0)
            json.dump(pokedex, f, indent=4)

    def battle(self):
        print(f"Un combat débute entre {self.pokemon1.get_name()} et {self.pokemon2.get_name()}!")
        while self.is_alive(self.pokemon1) and self.is_alive(self.pokemon2):
            attacker = random.choice([self.pokemon1, self.pokemon2])
            defender = self.pokemon1 if attacker == self.pokemon2 else self.pokemon2

            if not self.can_attack(attacker):
                print(f"{attacker.get_name()} a raté son attaque!")
                continue

            attack_power = attacker.attack_power

            if attacker.type == "Feu" and defender.type == "Terre":
                attack_power *= 1.5
            elif attacker.type == "Terre" and defender.type == "Eau":
                attack_power *= 1.5
            elif attacker.type == "Eau" and defender.type == "Feu":
                attack_power *= 1.5

            damage = max(attack_power - defender.defense, 1)
            defender.set_hp(defender.get_hp() - damage)
            print(f"{attacker.get_name()} inflige {damage} points de dégâts à {defender.get_name()}!")
        
        winner = self.get_winner()
        if winner is not None:
            print(f"{winner.get_name()} a gagné le combat!")
            self.record_pokedex(winner)
        else:
            print("Le combat s'est terminé en match nul.")

# Écrire des données dans un fichier JSON
data = {"nom": "Pikachu", "type": "électrique", "attaque": 55, "defense": 40}
with open("pokedex.json", "w") as f:
    json.dump(data, f, indent=4)

# Lire des données à partir d'un fichier JSON
with open("pokedex.json", "r") as f:
    data = json.load(f)
    print(data["nom"])  # affiche "Pikachu"
    print(data["type"])  # affiche "électrique"

combat = Combat(evoli, bulbizarre)
combat.battle()
