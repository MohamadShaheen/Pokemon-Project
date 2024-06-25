import json
import requests


def get_url():
    try:
        with open('../config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

    return config['poke_api_URL']


def get_pokemon_deta(pokemon_name):
    response = requests.get(f'{get_url()}/{pokemon_name.lower()}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_move_details(move_url):
    response = requests.get(move_url)
    if response.status_code == 200:
        return response.json()
    return None

def get_pokemon_details(pokemon_name):
    response = requests.get(f'{get_url()}/{pokemon_name.lower()}')
    if response.status_code == 200:
        data = response.json()
        types = [type_info['type']['name'] for type_info in data['types']]
        height = data['height']
        weight = data['weight']
        id = data['id']
        image = data['sprites']['other']['home']['front_default']
        return types, height, weight, id, image
    else:
        return None, None, None


def get_species_url(pokemon_name):
    data = get_pokemon_details(pokemon_name)
    if data:
        return data['species']['url']
    else:
        return None


def get_evolution_url(pokemon_name):
    species_url = get_species_url(pokemon_name)
    if species_url:
        response = requests.get(species_url)
        if response.status_code == 200:
            data = response.json()
            return data['evolution_chain']['url']
    return None


def get_evolved_pokemon(pokemon_name):
    evolution_url = get_evolution_url(pokemon_name)
    if evolution_url is None:
        return None

    response = requests.get(evolution_url)

    if response.status_code != 200:
        return None

    data = response.json()['chain']

    while data['species']['name'] != pokemon_name:
        if data['evolves_to']:
            data = data['evolves_to'][0]

    if len(data['evolves_to']) != 0:
        return data['evolves_to'][0]['species']['name']

    return None


def extract_attack_data(pokemon_name):
    pokemon_data = get_pokemon_deta(pokemon_name)
    if not pokemon_data:
        print("Failed to fetch Pokémon data.")
        return

    moves = [
        {
            "name": move["move"]["name"],
            "url": move["move"]["url"],
            "learn_method": move["version_group_details"][0]["move_learn_method"]["name"],
            "level_learned_at": move["version_group_details"][0]["level_learned_at"]
        }
        for move in pokemon_data.get("moves", [])
    ]

    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data.get("stats", [])}

    types = [t["type"]["name"] for t in pokemon_data.get("types", [])]

    print("Moves:")
    for move in moves:
        print(f" - {move['name'].title()} (Learned by {move['learn_method']} at level {move['level_learned_at']})")
    print("\nStats:")
    for stat, value in stats.items():
        print(f" - {stat.title()}: {value}")
    print("\nTypes:")
    print(" - " + ", ".join(types).title())


