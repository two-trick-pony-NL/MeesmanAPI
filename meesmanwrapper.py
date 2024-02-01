import requests
from bs4 import BeautifulSoup

class MeesmanClient:
    def __init__(self, username, password):
        self.session = self._get_session(username, password)

    def _get_session(self, username, password):
        url_login = "https://mijn.meesman.nl/login"

        payload = {
            'formdata[username]': username,
            'formdata[password][real]': password,
            'formdata[logout_every_session][value]': '1',
            'formdata[submit]': 'login-submit',
            'formdata[isSubmitted_loginform]': '1',
            'return_uri': '/'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        # Create a session
        session = requests.Session()
        
        # Login
        response = session.post(url_login, headers=headers, data=payload)

        # Check if login was successful based on the presence of a specific element
        if "accountOverviewTable" not in response.text:
            print("Login failed. Check your credentials.")
            return None
        
        return session

    def get_accounts(self):
        # Use the session to fetch the data from the authenticated page
        url = "https://mijn.meesman.nl"
        response = self.session.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with class 'meesmantable'
        table = soup.find('table', class_='meesmantable accountOverviewTable')

        # Extract data rows
        data_rows = []

        for row in table.find_all('tr')[1:]:  # Skip the first row as it contains headers
            # Extract the values from the row
            rekeningnummer = row.find('span', class_='accountNumber').text.strip()
            label = row.find('span', class_='accountLabel__editButtonText').text.strip()
            waarde = row.find('td', class_='right-aligned').find('span', class_='currency-symbol').text + \
                     row.find('td', class_='right-aligned').find('a').text.strip()
            
            waarde = waarde.replace('\xa0', '').replace('€', '')

            # Append the values to the data rows
            data_rows.append({rekeningnummer: {'label': label, 'euro_value':waarde}})

        return data_rows
    
    def get_resultaten(self):
        # Use the session to fetch the data from the authenticated page
        url = "https://mijn.meesman.nl/resultaten"
        response = self.session.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with class 'UnrealisedResultTable'
        table = soup.find('table', class_='UnrealisedResultTable')

        # Extract data rows
        data_rows = []

        for row in table.find_all('tr', class_='actual-data'):
            # Extract the values from the row
            fund = row.find('td', class_='name').text.strip()
            aanschafwaarde = row.find('td', {'data-th': 'Aanschafwaarde'}).text.strip()
            huidige_waarde = row.find('td', {'data-th': 'Huidige waarde'}).text.strip()
            ongerealiseerd_resultaat = row.find('td', {'data-th': 'Ongerealiseerd resultaat'}).text.strip()

            # Append the values to the data rows
            data_rows.append({
                'fund': fund,
                'aanschafwaarde': aanschafwaarde,
                'huidige_waarde': huidige_waarde,
                'ongerealiseerd_resultaat': ongerealiseerd_resultaat
            })

        return data_rows