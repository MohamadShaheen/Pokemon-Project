import pytest
from server import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.parametrize("pokemon_id", [1, 2, 3])
def test_get_pokemon_details_by_id(pokemon_id):
    response = client.get(f'/pokemons/?pokemon_id={pokemon_id}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Get pokemon details by id works successfully\n{response.text}\n')

@pytest.mark.parametrize("pokemon_name", ['bulbasaur', 'charmander', 'squirtle'])
def test_get_pokemon_details_by_name(pokemon_name):
    response = client.get(f'/pokemons/by-name/?pokemon_name={pokemon_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Get pokemon details by name works successfully\n{response.text}\n')

@pytest.mark.parametrize("pokemon_type", ['grass', 'fire', 'water'])
def test_get_pokemons_by_type(pokemon_type):
    response = client.get(f'/pokemons/by-type/?pokemon_type={pokemon_type}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Get pokemons by type works successfully\n{response.text}\n')

@pytest.mark.parametrize("trainer_name", ['Tierno', 'Ash', 'Brock'])
def test_get_pokemons_by_trainer(trainer_name):
    response = client.get(f'/pokemons/by-trainer/?trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Get pokemons by trainer works successfully\n{response.text}\n')

@pytest.mark.parametrize("pokemon_name", ['hoothoot'])
def test_add_new_pokemon(pokemon_name):
    response = client.post(f'/pokemons/?pokemon_name={pokemon_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Add pokemon works successfully\n{response.text}\n')

@pytest.mark.parametrize("pokemon_name", ['hoothoot'])
def test_delete_pokemon_by_name(pokemon_name):
    response = client.delete(f'/pokemons/?pokemon_name={pokemon_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Delete pokemon by name works successfully\n{response.text}\n')


def main():
    test_get_pokemon_details_by_id()
    test_get_pokemon_details_by_name()
    test_get_pokemons_by_type()
    test_get_pokemons_by_trainer()
    test_add_new_pokemon()
    test_delete_pokemon_by_name()


if __name__ == '__main__':
    main()
