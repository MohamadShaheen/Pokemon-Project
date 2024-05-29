from server import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_evolve_pokemon_of_trainer(pokemon_name: str, trainer_name: str):
    response = client.put(f'/evolve/?pokemon_name={pokemon_name}&trainer_name={trainer_name}')
    assert response.status_code == 200, f'Expected status_code 200 but got {response.status_code} - {response.text}'
    print(f'Evolve pokemon of trainer works successfully\n{response.text}\n')


def main():
    test_evolve_pokemon_of_trainer(pokemon_name='bulbasaur', trainer_name='Tierno')


if __name__ == '__main__':
    main()
