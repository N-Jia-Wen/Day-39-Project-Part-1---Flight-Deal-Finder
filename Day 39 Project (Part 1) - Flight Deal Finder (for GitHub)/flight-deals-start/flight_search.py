import requests
from datetime import datetime, timedelta
from flight_data import FlightData

IATA_CODE_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
DEAL_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
SEARCH_API_KEY = "Enter your Tequila Kiwi account's API key here."
HOME_LOCATION = "SIN"
CURRENCY = "SGD"
headers = {
    "apikey": SEARCH_API_KEY
}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.useful_data = None
        self.iata_code = None
        self.destination_codes_list = []
        self.current_time = datetime.now()
        self.earliest_dep_date = self.current_time.strftime("%d/%m/%Y")
        self.final_dep_date = (self.current_time + timedelta(6 * 30)).strftime("%d/%m/%Y")
        self.min_stay_length = 7
        self.max_stay_length = 28

    def find_iata_code(self, city_name):

        iata_code_parameters = {
            "term": city_name,
            "location_types": "city"
        }
        iata_code_response = requests.get(url=IATA_CODE_ENDPOINT, params=iata_code_parameters, headers=headers)
        city_data = iata_code_response.json()["locations"]
        self.iata_code = city_data[0]["code"]
        self.destination_codes_list.append(self.iata_code)

    def find_flight_deals(self, destination_code):
        flight_deal_parameters = {
            "fly_from": HOME_LOCATION,
            "fly_to": destination_code,
            "date_from": self.earliest_dep_date,
            "date_to": self.final_dep_date,
            "nights_in_dst_from": self.min_stay_length,
            "nights_in_dst_to": self.max_stay_length,
            "ret_from_diff_city": False,
            "ret_to_diff_city": False,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": CURRENCY
        }
        deal_response = requests.get(url=DEAL_ENDPOINT, params=flight_deal_parameters, headers=headers)
        try:
            deals_data = deal_response.json()["data"][0]
        except IndexError:
            print(f"No flight data to {destination_code} was found.")
            flight_data = None
        else:
            flight_data = FlightData(
                price=deals_data["price"],
                dep_city_name=deals_data["route"][0]["cityFrom"],
                dep_airport_code=deals_data["route"][0]["flyFrom"],
                arrival_city_name=deals_data["route"][0]["cityTo"],
                arrival_airport_code=deals_data["route"][0]["flyTo"],
                outbound_date=deals_data["route"][0]["local_departure"].split("T")[0],
                inbound_date=deals_data["route"][1]["local_arrival"].split("T")[0]
            )

        return flight_data
