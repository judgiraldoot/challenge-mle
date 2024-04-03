from typing import List

import uvicorn
import fastapi
import pandas as pd
from fastapi import HTTPException

from model import DelayModel

app = fastapi.FastAPI()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(data: dict) -> dict:

    TIPOVUELO = {'I', 'N'}
    OPERA = {'American Airlines', 'Air Canada', 'Air France', 'Aeromexico',
        'Aerolineas Argentinas', 'Austral', 'Avianca', 'Alitalia',
        'British Airways', 'Copa Air', 'Delta Air', 'Gol Trans', 'Iberia',
        'K.L.M.', 'Qantas Airways', 'United Airlines', 'Grupo LATAM',
        'Sky Airline', 'Latin American Wings', 'Plus Ultra Lineas Aereas',
        'JetSmart SPA', 'Oceanair Linhas Aereas', 'Lacsa'}
    MES = {1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12}
    
    df = pd.DataFrame(data["flights"])

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")
    elif not (set(df['TIPOVUELO']).issubset(TIPOVUELO) and set(df['OPERA']).issubset(OPERA) and set(df['MES']).issubset(MES)):
        raise HTTPException(status_code=400, detail="Unkown column provided")
    else:
        model = DelayModel()
        X = model.preprocess(df)
        predictions = model.predict(X)
    
    return {"predict": predictions}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)