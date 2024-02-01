from fastapi import FastAPI
from meesmanwrapper import MeesmanClient
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("MEESMAN_USERNAME")
password = os.getenv("MEESMAN_PASSWORD")

meesman_client = MeesmanClient(username, password)

app = FastAPI()


@app.get("/accounts")
def read_root():
    accounts = meesman_client.get_accounts()
    
    return {"accounts": accounts}

@app.get("/resultaten")
def read_root():
    resultaten = meesman_client.get_resultaten()
    return {"resultaten": resultaten}