from fastapi import FastAPI, HTTPException, Header, Depends, Form
from meesmanwrapper import MeesmanClient
from mangum import Mangum
from authentication import obtain_token, obtain_credentials




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


@app.post("/getauthtoken")
async def submit_credentials(username: str = Form(...), password: str = Form(...)):
    
    meesman_client = MeesmanClient(username, password)
    valid = meesman_client._get_session(username, password)
    
    if not valid: 
        raise HTTPException(status_code=404, detail="No account found")

    token = obtain_token(username, password)
    
    # Return a success message
    return {"authtoken": token}

    
    
@app.get("/getmeesmandata")
def combined(token: str):
    # Validate the token or perform any necessary checks
    print('This token', token)
    try:
        username, password = obtain_credentials(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Use your MeesmanClient to fetch data
    meesman_client = MeesmanClient(username, password)
    result = {
        'waardeontwikkeling': meesman_client.get_waarde_ontwikkeling(),
        'historic_data': meesman_client.get_historic_value(),
        'portefeuille': meesman_client.get_portefeuille(),
        'resultaten': meesman_client.get_resultaten(),
        'accounts': meesman_client.get_accounts(),
    }
    return result
        
        
    
    
    # Return a success message

handler = Mangum(app)
