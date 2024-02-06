from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from meesmanwrapper import MeesmanClient
from mangum import Mangum
from constants import API_KEY, MEESMAN_PASSWORD, MEESMAN_USERNAME
import os

username = MEESMAN_USERNAME
password = MEESMAN_PASSWORD


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
    print("Healthcheck ran")
    return "Up and running"

@app.get("/")
def meesman(
    username: str = Header(..., convert_underscores=False),
    password: str = Header(..., convert_underscores=False),
    ):
    print("New request came in...")
    try:
        session = MeesmanClient(password=password, username=username)
        result = {
            'waardeontwikkeling': session.get_waarde_ontwikkeling(),
            'historic_data': session.get_historic_value(),
            'portefeuille': session.get_portefeuille(),
            'resultaten': session.get_resultaten(),
            'accounts': session.get_accounts(),
        }
        print("Found user: ", username, " retrieving their data from Meesman")
        print("Returning result:")
        return result
    except Exception as e:
        print("User not found:")
        print(e)
        return HTTPException(status_code=401, detail="Incorrect password or username")

@app.get("/dummy")
def dummydata():
    return FileResponse("dummy.json", media_type="application/json")

@app.get("/combined")
def combined():
    meesman_client = MeesmanClient(username, password)
    result = {
        'waardeontwikkeling': meesman_client.get_waarde_ontwikkeling(),
        'historic_data': meesman_client.get_historic_value(),
        'portefeuille': meesman_client.get_portefeuille(),
        'resultaten': meesman_client.get_resultaten(),
        'accounts':meesman_client.get_accounts(),
    }
    return result

handler = Mangum(app)
