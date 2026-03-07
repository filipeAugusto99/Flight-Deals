#This file will need to use the DataManager,FlightSearch, FlightData,  classNotificationManageres to achieve the program requirements.
import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


# ==================== Set up the Flight Search ====================
dm = DataManager()
sheet_data = dm.get_destination_data()
fs = FlightSearch()
nfm = NotificationManager()


# Set origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

#  In main.py check if sheet_data contains any values for the "iataCode" key.
#  If not, then the IATA Codes column is empty in the Google Sheet.
#  In this case, pass each city name in sheet_data one-by-one
#  to the FlightSearch class to get the corresponding IATA code
#  for that city using the API.
#  You should use the code you get back to update the sheet_data dictionary.

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = fs.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

# ==================== Search for Flights ====================

tomorrow = datetime.now() + timedelta(days=1)
one_month = datetime.now() + timedelta(days=(1 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")

    flights = fs.get_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time= tomorrow,
        to_time=one_month
    )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")
        nfm.send_sms(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
        # SMS not working? Try whatsapp instead.
        # nfm.send_whatsapp(
        #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )
    # slowing down requests to avoid rate limit
    time.sleep(2)

# dm.destination_data = sheet_data
# dm.update_iata_code()