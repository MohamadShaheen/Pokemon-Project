import random
import json
from utils.api_operations import get_pokemon_deta, fetch_move_details, extract_attack_data


class Battle:
    def __init__(self, pokemon1_name, pokemon2_name):
        self.pokemon1 = get_pokemon_deta(pokemon1_name)
        self.pokemon2 = get_pokemon_deta(pokemon2_name)
        if not self.pokemon1 or not self.pokemon2:
            raise ValueError("Could not fetch details for one or both Pokémon.")

        self.battle_log = {
            'pokemon1': pokemon1_name,
            'pokemon2': pokemon2_name,
            'moves': [],
            'winner': None
        }

    def attack(self, attacker, defender):
        if not attacker['moves']:
            return 0

        move = random.choice(attacker['moves'])
        move_details = fetch_move_details(move['move']['url'])
        if not move_details or not move_details.get('power'):
            return 0

        # Random factor to simulate battle conditions and variability
        random_factor = random.uniform(0.85, 1.0)  # Typically, damage variability

        power = move_details['power']
        attack_stat = attacker['stats'][1]['base_stat']
        defense_stat = defender['stats'][2]['base_stat']
        damage = ((2 * power * (attack_stat / defense_stat)) // 50) + 2
        damage*=random_factor

        self.battle_log['moves'].append({
            'attacker': attacker['name'],
            'defender': defender['name'],
            'move': move['move']['name'],
            'damage': damage
        })
        return damage

    def simulate_battle(self):
        if not self.pokemon1 or not self.pokemon2:
            return "Battle cannot be conducted due to missing Pokémon data."

        p1_hp = self.pokemon1['stats'][0]['base_stat']  # Assuming 'hp' is always the first stat
        p2_hp = self.pokemon2['stats'][0]['base_stat']

        while p1_hp > 0 and p2_hp > 0:
            p2_hp -= self.attack(self.pokemon1, self.pokemon2)
            if p2_hp <= 0:
                winner = self.pokemon1['name']
                break

            p1_hp -= self.attack(self.pokemon2, self.pokemon1)
            if p1_hp <= 0:
                winner = self.pokemon2['name']
                break

        if p1_hp == p2_hp:
            winner = 'Tie'
        else:
            winner = self.pokemon1['name'] if p1_hp > p2_hp else self.pokemon2['name']

        self.battle_log['winner'] = winner
        return self.battle_log


# if __name__ == "__main__":
#     battle = Battle("hoothoot", "pikachu")
#     # extract_attack_data("ditto")
#     # extract_attack_data("pikachu")
#     result = battle.simulate_battle()
#     print(f"Winner of the battle: {result}")
