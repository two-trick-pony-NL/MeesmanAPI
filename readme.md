<img src="https://github.com/two-trick-pony-NL/MeesmanUnofficialApp/assets/71013416/8fde4da7-5b18-4cfe-aadd-440d4f85ba80" height="400">
<img src="https://github.com/two-trick-pony-NL/MeesmanUnofficialApp/assets/71013416/5c3f5419-1804-49b0-a543-ec3c8f03596f" height="400">
<img src="https://github.com/two-trick-pony-NL/MeesmanUnofficialApp/assets/71013416/0b1d5fb8-108e-4d5a-8c61-ae43b43d55dc" height="400">
<img src="https://github.com/two-trick-pony-NL/MeesmanUnofficialApp/assets/71013416/70ac6468-ef67-4a4b-b4e2-12ad0500c29b" height="400">



# Meesman API

This Python API wrapper facilitates programmatic access to the Meesman Indexbeleggen platform, allowing users to fetch account details. It's designed to run from AWS Lambda functions, leveraging the infrequent need for updates as Meesman typically invests once a week. This makes it a very cost effective way to run this API. 

## Features
You can retrieve the following information:
- **Login:** Securely can log you in by using security Tokens stored on the client side
- **Accounts:** Lists your accounts, balances, and labels.
- **Resultaten:** Displays the results of your investments.
- **Portfolio:** Lists your current portfolio.
- **Historic Data:** Provides a list of dates and balances, useful for graphing.
- **Value Development:** Illustrates how your balance has grown year over year.

## Companion App:
A companion app built with React Native is available [here](https://github.com/two-trick-pony-NL/MeesmanUnofficialApp). This app allows you to interact with the Meesman API through a user-friendly interface from a Android or iOS device in the form of an app.


## How to Run

1. Follow the [installation instructions](https://ademoverflow.com/blog/tutorial-fastapi-aws-lambda-serverless/) provided in this [blog post](https://ademoverflow.com/blog/tutorial-fastapi-aws-lambda-serverless/) to set up your AWS Lambda environment.

2. After setting up permissions, deploy using Serverless Framework:
    - To update:
      ```bash
      sls deploy --stage staging
      ```
    - To delete:
      ```bash
      sls remove --stage staging
      ```

3. For local development, run:
   
    ```
    uvicorn main:app --reload
    ```
    
    Then to get a token:
   - go to: localhost:8000/docs

  
<img width="556" alt="Screenshot 2024-02-13 at 13 58 45" src="https://github.com/two-trick-pony-NL/MeesmanAPI/assets/71013416/8c4ea96b-5be4-417e-a6ae-b187d94e465a">


   - Use the authtoken endpoint to submit your username and password, the backend will return you a token.
     <img width="554" alt="Screenshot 2024-02-13 at 13 59 18" src="https://github.com/two-trick-pony-NL/MeesmanAPI/assets/71013416/7a5d3a8c-deca-469d-b0f2-a25e8e57cca1">
     This should return something like this
  
     
     ```
     {
          "authtoken": "gAAAAABly2fViwFPwuqf-NEA9P-gD3QfscRomkr16KP7BfxItlETOo8pyeKTIvEvBPShV_BoVJ3N7m9c9PMTVtvpd87BdCc7vXVMymAiSWTq_t_-Als0f6w=gAAAAABly2fVRwK5Atj5ECN2dNpEjX8usFwQwnbOIGohf0sAq0pCTGxzUoWhmZE3J9pNVjyQnJ29yyoiKHqFZXsxwXO3xb291wBWVMnk1-rkVrpvEKk26ok1"
        }

     ```

   - Use the token you receive in the `getmeesmandata` endpoint

## To Do
- Extend data scraping to handle multiple accounts. Currently only data from your 1st account is returned. Open an issue if you would like this feature. 

## Disclaimer

**I am not affiliated with Meesman.**
This API is a personal project created by a Meesman customer to visualize investments via an app, requiring an API for data retrieval.

**Use at Your Own Risk:**
The software comes as-is, and its use is at your own risk. Bugs or errors may exist that could lead to financial loss or unintended consequences.

**Real Money and Real Passwords:**
This API interacts with real financial data and requires genuine login credentials. Exercise caution, recognizing that actions performed using this code involve real money and personal account information.

**No Warranty or Guarantee:**
There is no warranty or guarantee, expressed or implied. The author and contributors are not responsible for any damages or losses incurred through the use of this software.

**Security Considerations:**
Review and understand the security implications of using this software. Protect sensitive information such as API keys and passwords. Never share credentials or API keys publicly.

By using this Meesman API Wrapper, you acknowledge and accept the risks involved. Always double-check the code, keep credentials secure, and use it responsibly.
