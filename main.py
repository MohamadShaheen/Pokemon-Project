import json
from utils.api_operations import get_pokemon_details
from database_connection import create_database


def edit_json_file(config):
    if config['database_editor'] == 0:
        with open('data/pokemons_data.json', 'r') as file:
            pokemon_data = json.load(file)

        for pokemon in pokemon_data:
            correct_types, _, _ = get_pokemon_details(pokemon['name'])
            if correct_types:
                pokemon['types'] = correct_types
                if 'type' in pokemon:
                    del pokemon['type']

        with open('data/pokemons_data.json', 'w') as file:
            json.dump(pokemon_data, file, indent=4)

        config['database_editor'] = 1
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print('Database already up to date')


def create_sql_database(config):
    if config['create_database'] == 0:
        create_database.create_database()

        config['create_database'] = 1
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print('Database already created')


def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    edit_json_file(config)
    create_sql_database(config)


if __name__ == '__main__':
    main()
