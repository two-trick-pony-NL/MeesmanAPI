from fastapi import FastAPI, HTTPException, Header, Depends, Form, Query
from meesmanwrapper import MeesmanClient
from mangum import Mangum
from authentication import obtain_token, obtain_credentials
from pushnotifications import send_push_message, save_to_dynamodb, get_all_strings_from_dynamodb




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
        
        
    
    
@app.get("/sendpushmessage")
async def sendpushmessage(
    token: str = Query(..., title="User Token", description="User authentication token"),
    title: str = Query(..., title="Post Title", description="Title of the post"),
    body: str = Query(..., title="Post Body", description="Body content of the post"),
    ):
    push_succesful = send_push_message(token, title, body)
    if push_succesful:
        result = {"status": 'success', "token": token, "title": title, "body": body}
        return result
    else:
        raise HTTPException(status_code=500, detail="Push message failed to be transmitted")
    
@app.get("/sendpushmessagetoall")
async def sendbulkpushmessages(
    title: str = Query(..., title="Post Title", description="Title of the post"),
    body: str = Query(..., title="Post Body", description="Body content of the post"),
    ):
    count = 0
    known_push_tokens = get_all_strings_from_dynamodb()
    for token in known_push_tokens:
        count =+ 1
        try:
            send_push_message(token, title, body)
        except:
            print('Could not send to: ', token)
    
    result = {"status": 'success', "total messages sent": count, "title": title, "body": body}
    return result

@app.get("/registerpushtoken")
async def registerpushtoken(
    token: str = Query(..., title="Push Token", description="The push token of a devide "),
    ):
    save_to_dynamodb(token)
    result = {"status": 'success', 'token':token}
    return result
            
    
        

        

handler = Mangum(app)
