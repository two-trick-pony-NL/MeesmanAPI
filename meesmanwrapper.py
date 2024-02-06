from bs4 import BeautifulSoup
import re
import lambda_requests as requests

class MeesmanClient:
    def __init__(self, username, password):        
        self.session = self._get_session(username, password)
        self.username = username
        self.password = password

    def _get_session(self, username, password):
        print("Creating session at Meesman")
        try:
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
                print("Login to Meesman failed. Check your credentials.")
                return None
                    
            return session
        except Exception as e:
            return e
    
    def get_accounts(self):
        print("Obtaining accounts")
        try: 
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
        except Exception as e:
            return e
        
    
    def get_portefeuille(self):
        print("Obtaining portfolio")
        try: 
            # Use the session to fetch the data from the authenticated page
            url = "https://mijn.meesman.nl/portefeuille"
            response = self.session.get(url)
            
            # Check if the request was successful
            if response.status_code != 200:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table with class 'PortfolioTable'
            table = soup.find('table', class_='PortfolioTable')

            # Extract data rows for the specific funds
            specific_funds = []

            for row in table.find_all('tr', class_='actual-data'):
                # Extract the values from the row
                fund = row.find('td', class_='name').text.strip()
                if fund in ['Aandelen Wereldwijd Totaal', 'Obligaties Wereldwijd (wordt gesloten)']:
                    aantal = row.find('td', {'data-th': 'Aantal'}).text.strip()
                    koers = row.find('td', {'data-th': 'Koers'}).text.strip()
                    datum = row.find('td', {'data-th': 'Valutadatum'}).text.strip()
                    waarde = row.find('td', {'data-th': 'Waarde'}).text.strip()
                    actuele_weging = row.find('td', {'data-th': 'Actuele weging'}).text.strip()

                    # Append the values to the specific_funds list
                    specific_funds.append({
                        'fund': fund,
                        'aantal': aantal,
                        'koers': koers,
                        'datum': datum,
                        'waarde': waarde,
                        'actuele_weging': actuele_weging
                    })
            return specific_funds
        except Exception as e:
            return e
      
    def get_resultaten(self):
        print("Getting results")
        try: 
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
        except Exception as e:
            return e
    
    def get_historic_value(self):
        print("Obtaining historic values")
        try:
            url = "https://mijn.meesman.nl/waardeontwikkeling"
            response = self.session.get(url)

            # Check if the request was successful
            if response.status_code != 200:
                return f"Failed to fetch data. Status code: {response.status_code}"

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', text=re.compile(r'var Chart = new PortfolioChart\(\);'))

            # Extract the script content
            script_content = script_tag.text if script_tag else None

            # Use regex to extract the list of historic values
            match = re.search(r'\[\[.*?\]\]\s*,\s*\[\[.*?\]\]', script_tag.text) if script_tag else None
            historic_values_list = eval(match.group()) if match else None

            return historic_values_list
        except Exception as e:
            return e
    
    def get_waarde_ontwikkeling(self):
        print("Obtaining value development")
        try:
            # Use the session to fetch the data from the authenticated page
            url = "https://mijn.meesman.nl/waardeontwikkeling"
            response = self.session.get(url)

            # Check if the request was successful
            if response.status_code != 200:
                return f"Failed to fetch data. Status code: {response.status_code}"

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all tables with the specified class
            tables = soup.find_all('table', class_='meesmantable PortfolioResultTable__content')

            result = []

            for table in tables[1:]:
                table_data = {"columns": [], "data": []}

                # Extract column names
                columns = [th.text.strip() for th in table.select('thead th.PortfolioResultTable__headTitle')]
                table_data["columns"] = columns

                # Extract row data
                rows = table.select('tbody tr.actual-data')
                for row in rows:
                    row_data = [td.text.strip() for td in row.find_all('td')]
                    table_data["data"].append(row_data)

                result.append(table_data)

            return(result)
        except Exception as e:
            return e
