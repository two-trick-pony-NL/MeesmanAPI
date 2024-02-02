# Meesman API
This is a Python API wrapper for the Meesman Indexbeleggen platform. The basic idea is to be able to fetch your account details programatically. 

You'll be able to fetch the following information: 
- Accounts: Lists your accounts, balance and labels
- Resultaten: lists the results of your investments
- Portfolio: lists your portfolio
- Historic Data: Shows a list of dates and balances. This can be used to draw a graph
- Value development: How your balance grew year over year

## How to run
1. The project revolves around FastAPI. When calling endpoints we scrape the Meesman Website to extract data and return that in JSON format. 
2. So install the `requirements.txt` file to get dependancies
3. Create a `.env` file in the root with the following structure: 
```
MEESMAN_USERNAME='youremail@address.com'
MEESMAN_PASSWORD='meesmanpassword'
API_KEY='yourpasswordfortheapi'
```
4. run `uvicorn main:app` this will start the server on port 8000
The API_KEY you set in your environment will be the password to make API calls. This ensures not everyone can see your balance. 

## To do
- If you have multiple accounts I do not yet scrape all the data for those accounts. 

## Disclaimer

**I am not affiliated with Messman**
I'm just a customer that wants to see my investments from an app and thus needed an API. 

**Use at Your Own Risk:**
This software is provided as-is, and the use of this API wrapper is at your own risk. The code may have bugs or errors that could potentially lead to financial loss or other unintended consequences.

**Real Money and Real Passwords:**
This API wrapper interacts with real financial data and requires real login credentials. Exercise caution and be aware that any actions performed using this code are associated with real money and personal account information. 

**No Warranty or Guarantee:**
There is no warranty or guarantee of any kind, expressed or implied. The author and contributors are not responsible for any damages or losses incurred through the use of this software.

**Security Considerations:**
It is crucial to review and understand the security implications of using this software. Be sure to protect sensitive information, such as API keys and passwords. Never share your credentials or API keys publicly.

By using this Meesman API Wrapper, you acknowledge and accept the risks involved. Always double-check the code, keep your credentials secure, and use it responsibly.
