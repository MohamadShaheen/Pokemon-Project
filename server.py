import os
import uvicorn
from main import main
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import pokemons_router, evolve_router, trainers_router, images_router, trade_router, battle_router

load_dotenv()

host = os.getenv('SERVER_HOST')
port = os.getenv('SERVER_PORT')

app = FastAPI()


@app.get('/')
async def root():
    return f'Are you that Naive and old fashion? Go to {host}:{port}/docs for better experience'


app.include_router(pokemons_router.router, prefix='/pokemons', tags=['Pokemon Endpoints'])
app.include_router(trainers_router.router, prefix='/trainers', tags=['Trainer Endpoints'])
app.include_router(evolve_router.router, prefix='/evolve', tags=['Evolution Endpoints'])
app.include_router(images_router.router, prefix='/images', tags=['Image Endpoints'])
app.include_router(trade_router.router, prefix='/trade', tags=['Trade Endpoints'])
app.include_router(battle_router.router, prefix='/battle', tags=['Battle Endpoints'])


if __name__ == '__main__':
    main()
    uvicorn.run(app, host='0.0.0.0', port=int(port))
