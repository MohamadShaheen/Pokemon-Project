import pytest

from server import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.parametrize("pokemon_name, trainer_name", [('bulbasaur', 'Tierno')])
def test_delete_pokemon_of_trainer(pokemon_name: str, trainer_name: str):
    response = client.put(f'/trainers/?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Delete pokemon of trainer works successfully\n{response.text}\n')

@pytest.mark.parametrize("pokemon_name", ['bulbasaur'])
def test_get_pokemon_trainers(pokemon_name: str):
    response = client.get(f'/trainers/?pokemon_name={pokemon_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Get pokemon trainers works successfully\n{response.text}\n')

@pytest.mark.parametrize("pokemon_name, trainer_name", [('bulbasaur', 'Tierno')])
def test_add_pokemon_to_trainer(pokemon_name: str, trainer_name: str):
    response = client.post(f'/trainers/pokemon/?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Add pokemon to trainer works successfully\n{response.text}\n')

@pytest.mark.parametrize("trainer_name, trainer_town", [('Mohamad Shaheen', 'Sakhnin')])
def test_create_trainer(trainer_name: str, trainer_town: str):
    response = client.post(f'/trainers/trainer/?trainer_name={trainer_name}&trainer_town={trainer_town}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Create trainer works successfully\n{response.text}\n')

@pytest.mark.parametrize("trainer_name", ['Mohamad Shaheen'])
def test_delete_trainer_by_name(trainer_name: str):
    response = client.delete(f'/trainers/?trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Delete trainer by name works successfully\n{response.text}\n')


def main():
    test_delete_pokemon_of_trainer()
    test_get_pokemon_trainers()
    test_add_pokemon_to_trainer()
    test_create_trainer()
    test_delete_trainer_by_name()


if __name__ == '__main__':
    main()
