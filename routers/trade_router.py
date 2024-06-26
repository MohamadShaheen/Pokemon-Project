from fastapi import APIRouter, HTTPException
from DAL.trade_interactor import TradeInteractor

router = APIRouter()


@router.put('/')
async def trade(trainer1_name: str, pokemon1_name: str, trainer2_name: str, pokemon2_name: str, trainer2_response: str):
    trade_interactor = TradeInteractor()
    response = trade_interactor.trade(trainer1_name, pokemon1_name, trainer2_name, pokemon2_name, trainer2_response)

    if response == 1:
        raise HTTPException(status_code=404, detail=f'Trainer {trainer1_name} does not exist')

    elif response == 2:
        raise HTTPException(status_code=404, detail=f'Trainer {trainer2_name} does not exist')

    elif response == 3:
        raise HTTPException(status_code=404, detail=f'{trainer1_name} does not have {pokemon1_name} in his collection')

    elif response == 4:
        raise HTTPException(status_code=404, detail=f'{trainer2_name} does not have {pokemon2_name} in his collection')

    elif response == 5:
        raise HTTPException(status_code=409, detail=f'{trainer2_name} already has {pokemon1_name} in his collection')

    elif response == 6:
        raise HTTPException(status_code=409, detail=f'{trainer1_name} already has {pokemon2_name} in his collection')

    elif response == 7:
        return f'{trainer2_name} rejected the trade'

    return response
