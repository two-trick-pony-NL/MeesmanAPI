from fastapi import FastAPI, Depends, HTTPException, status
from meesmanwrapper import MeesmanClient
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv


import os

load_dotenv()
username = os.getenv("MEESMAN_USERNAME")
password = os.getenv("MEESMAN_PASSWORD")

# Define API key header
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)



# Dependency to validate API key
async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

# A class that creates a session for
meesman_client = MeesmanClient(username, password)

app = FastAPI(
    title="Meesman API Wrapper",
    description="API wrapper for Meesman, providing endpoints to access account information, results, portfolio, historic data, and asset value development.",
    version="1.0",
)


@app.get("/")
def root():
    """
    Root endpoint to check if the API is up and running.
    """
    return "Up and running"

@app.get("/accounts")
def accounts(api_key: str = Depends(get_api_key)):
    """
    Get a list of accounts from Meesman.
    """
    accounts = meesman_client.get_accounts()
    return {"accounts": accounts}

@app.get("/resultaten")
def resultaten(api_key: str = Depends(get_api_key)):
    """
    Get result data from Meesman.
    """
    resultaten = meesman_client.get_resultaten()
    return {"resultaten": resultaten}

@app.get("/portefeuille")
def portfolio(api_key: str = Depends(get_api_key)):
    """
    Get portfolio data from Meesman.
    """
    portefeuille = meesman_client.get_portefeuille()
    return {"portefeuille": portefeuille}

@app.get("/historic_data")
def historic_data(api_key: str = Depends(get_api_key)):
    """
    Get historic data from Meesman.
    """
    data = meesman_client.get_historic_value()
    return {"historic_data": data}

@app.get("/waardeontwikkeling")
def waardeontwikkeling(api_key: str = Depends(get_api_key)):
    """
    Get development of asset value over time from Meesman.
    """
    data = meesman_client.get_waarde_ontwikkeling()
    return {"waardeontwikkeling": data}
