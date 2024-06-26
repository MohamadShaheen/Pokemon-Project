import json
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


def get_url():
    try:
        with open('../config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

    return config['poke_api_URL']


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
    response = requests.get(f'{get_url()}/{pokemon_name.lower()}')
    if response.status_code == 200:
        data = response.json()
        species_url = data['species']['url']
        return species_url
    else:
        return None


def get_evolution_url(pokemon_name):
    species_url = get_species_url(pokemon_name)
    if species_url is None:
        return None

    response = requests.get(species_url)
    if response.status_code == 200:
        data = response.json()
        evolution_url = data['evolution_chain']['url']
        return evolution_url
    else:
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


def get_trainers_url():
    try:
        with open('../config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

    return config['trainers_api_URL']


def get_trainer_image_url(trainer_name):
    response = requests.get(f'{get_trainers_url()}/{trainer_name}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find('a', class_='image')
        if image_tag and image_tag.img:
            image_url = image_tag.img['srcset'].split()[0]
            return image_url
        else:
            return None
    else:
        return None
