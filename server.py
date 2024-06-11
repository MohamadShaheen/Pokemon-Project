import os
from time import sleep

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import pokemons_router, evolve_router, trainers_router
import main as m
# from database_connection import models

load_dotenv()

host = os.getenv('SERVER_HOST')
port = os.getenv('SERVER_PORT')

app = FastAPI()


app.include_router(pokemons_router.router, prefix='/pokemons')
app.include_router(trainers_router.router, prefix='/trainers')
app.include_router(evolve_router.router, prefix='/evolve')


@app.get('/')
def root():
    return f'Are you that Naive and old fashion? Go to {host}:{port}/docs for better experience'



if __name__ == "__main__":
    # for docker
    m.main()
    sleep(30)
    uvicorn.run(app, host="0.0.0.0", port=8000)