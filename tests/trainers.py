from server import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_delete_pokemon_of_trainer(pokemon_name: str, trainer_name: str):
    response = client.put(f'/trainers/?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Delete pokemon of trainer works successfully\n{response.text}\n')


def test_get_pokemon_trainers(pokemon_name: str):
    response = client.get(f'/trainers/?pokemon_name={pokemon_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Get pokemon trainers works successfully\n{response.text}\n')


def test_add_pokemon_to_trainer(pokemon_name: str, trainer_name: str):
    response = client.post(f'/trainers/pokemon/?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Add pokemon to trainer works successfully\n{response.text}\n')


def test_create_trainer(trainer_name: str, trainer_town: str):
    response = client.post(f'/trainers/trainer/?trainer_name={trainer_name}&trainer_town={trainer_town}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Create trainer works successfully\n{response.text}\n')


def test_delete_trainer_by_name(trainer_name: str):
    response = client.delete(f'/trainers/?trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Delete trainer by name works successfully\n{response.text}\n')


def main():
    test_delete_pokemon_of_trainer(pokemon_name='bulbasaur', trainer_name='Tierno')
    test_get_pokemon_trainers(pokemon_name='bulbasaur')
    test_add_pokemon_to_trainer(pokemon_name='bulbasaur', trainer_name='Tierno')
    test_create_trainer(trainer_name='Mohamad Shaheen', trainer_town='Sakhnin')
    test_delete_trainer_by_name(trainer_name='Mohamad Shaheen')


if __name__ == '__main__':
    main()
