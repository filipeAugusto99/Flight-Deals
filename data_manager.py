import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


SHEETY_END_POINT = "https://api.sheety.co/e21a8e91526b16245a7b34dab6850543/flightDeals/prices"


class DataManager:
    def __init__(self):
        self._user = os.environ["USER"]
        self._password = os.environ["PASSW"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}


    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_END_POINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes.
    def update_iata_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            sheet_response = requests.put(
                url=f"{SHEETY_END_POINT}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            print(sheet_response.text)