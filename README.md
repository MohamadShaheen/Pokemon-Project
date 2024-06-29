# Pokemon Project

This project represents a simple server that allows interaction with a database of Pokemon. One can view, search, and filter Pokemon information through the terminal or the FastAPI interface.

## Features

- Search Pokemon by id or name
- Search all Pokemons by trainer or type
- Search all trainers of a specific Pokemon
- Add new Pokemon using external API
- Add new trainer
- Add Pokemon to trainer
- Delete Pokemon or trainer
- Delete Pokemon from trainer
- Evolve Pokemon of specific trainer
- Battle Pokemon
- Battle Trainer with specific pokemon
  
## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- PyMySQL
- Requests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/MohamadShaheen/Pokemon-Project.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Pokemon-Project
    ```
3. Create and activate a virtual environment:
    ```sh
    python -m venv env
    source env/Scripts/activate  # On Mac use `env\bin\activate`
    ```
4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Database Setup

1. Ensure PyMySQL is installed and running.
2. Create a new database scheme for the project (recommended: with the name `pokemonsdatabase`).
3. Create `.env` file for the project:
   ```
   DATABASE_USERNAME=[YOUR DATABASE USERNAME]
   DATABASE_PASSWORD=[YOUR DATABASE PASSWORD]
   DATABASE_HOST=[YOUR DATABASE HOST]
   DATABASE_PORT=[YOUR DATABASE PORT]
   DATABASE_NAME=[YOUR SCHEME NAME]
   SERVER_HOST=[YOUR SERVER HOST]
   SERVER_PORT=[YOUR SERVER PORT]
   ```
4. Update the `config.json` file:
   ```
   {
    "poke_api_URL": "https://pokeapi.co/api/v2/pokemon",
    "database_editor": 0,
    "create_database": 0
   }
   ```
5. Run the `database_connection/models.py` to set up the database tables.
6. Run the `main.py` to fill the database tables:
    ```sh
    python main.py
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn server:app --reload
    ```

## Testing

1. To run the tests, you can run each of the following:
    ```
    tests/pokemons.py
    tests/trainers.py
    tests/evolve.py
    ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact

For any questions or inquiries, please contact [Mohamad Shaheen](https://github.com/MohamadShaheen).
