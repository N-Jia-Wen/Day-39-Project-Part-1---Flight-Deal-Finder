import requests

SHEETY_ENDPOINT = ("Enter your Google sheet's endpoint (given by Sheety) here.")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        get_response = requests.get(url=SHEETY_ENDPOINT)
        self.sheet_data = get_response.json()["flightDeals"]

    def update_sheet(self, updated_vacation_destination):
        # After self.sheet_data dictionary is updated in main.py, execute this:

        id_num = updated_vacation_destination["id"]
        specific_sheety_endpoint = f"{SHEETY_ENDPOINT}/{id_num}"
        changed_data = {
            "flightDeal": {
                "iataCode": updated_vacation_destination["iataCode"]
            }
        }
        put_response = requests.put(url=specific_sheety_endpoint, json=changed_data)
        put_response.raise_for_status()
