import random

from DAL.pokemon_battle_interactor import Battle


class TrainerBattle:
    def __init__(self, trainer1_name, trainer2_name, trainer1_pokemons, trainer2_pokemons):
        self.trainer1_name = trainer1_name
        self.trainer2_name = trainer2_name
        self.trainer1_pokemons = trainer1_pokemons
        self.trainer2_pokemons = trainer2_pokemons

        self.battle_log = {
            'trainer1': trainer1_name,
            'trainer2': trainer2_name,
            'rounds': [],
            'winner': None
        }

    def simulate_battle(self):
        #if both trainers have no pokemons then its a tie
        if not self.trainer1_pokemons and not self.trainer2_pokemons:
            return self.battle_log

        #if one has pokemnos and the other doessnt then hes the winner
        if not self.trainer1_pokemons:
            self.battle_log['winner'] = self.trainer2_name
            return self.battle_log
        if not self.trainer2_pokemons:
            self.battle_log['winner'] = self.trainer1_name
            return self.battle_log

        #if both have pokemons then
        while self.trainer1_pokemons and self.trainer2_pokemons:
            # Randomly select a Pokémon from each trainer's list

            pokemon1 = random.choice(self.trainer1_pokemons)
            pokemon2 = random.choice(self.trainer2_pokemons)

            Fight = Battle(pokemon1, pokemon2)
            round_result = Fight.simulate_battle()
            self.battle_log['rounds'].append(round_result)

            if 'winner' in round_result:
                if round_result['winner'] == pokemon1:
                    self.trainer2_pokemons.remove(pokemon2)
                else:
                    self.trainer1_pokemons.remove(pokemon1)
            else:
                print("Error: Expected round_result to be a dictionary with a 'winner' key.")


        if self.trainer1_pokemons:
            self.battle_log['winner'] = self.trainer1_name
        else:
            self.battle_log['winner'] = self.trainer2_name

        return self.battle_log

# if __name__ == "__main__":
#     battle = TrainerBattle("Tierno", "Archie", ["hoothoot"], ["pikachu"])
#     result = battle.simulate_battle()
#     print(f"Winner of the battle: {result}")
