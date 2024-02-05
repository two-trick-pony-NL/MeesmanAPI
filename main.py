from fastapi import FastAPI, HTTPException, status, Header
from meesmanwrapper import MeesmanClient
from fastapi.security import APIKeyHeader
from mangum import Mangum
import os


app = FastAPI(
    title="Meesman API Wrapper",
    description="API wrapper for Meesman, providing endpoints to access account information.",
    version="1.0",
)


@app.get("/healthcheck")
def root():
    """
    Root endpoint to check if the API is up and running.
    """
    return "Up and running"

@app.get("/")
def meesman(
    username: str = Header(..., convert_underscores=False),
    password: str = Header(..., convert_underscores=False)
    ):
    print(username)
    print(password)
    try:
        session = MeesmanClient(password=password, username=username)
        result = {
            'waardeontwikkeling': session.get_waarde_ontwikkeling(),
            'historic_data': session.get_historic_value(),
            'portefeuille': session.get_portefeuille(),
            'resultaten': session.get_resultaten(),
            'accounts': session.get_accounts(),
        }
        return result
    except Exception as e:
        print(e)
        return HTTPException(status_code=401, detail="Incorrect password or username")



handler = Mangum(app)
