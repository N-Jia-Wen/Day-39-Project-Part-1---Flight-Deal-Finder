from twilio.rest import Client

TWILIO_ACC_SID = "Enter your Twilio account's SID here."
TWILIO_AUTH_TOKEN = "Enter your Twilio authentication token here."
TWILIO_PHONE_NO = "Enter your virtual Twilio phone number here."
VERIFIED_PHONE_NO = "Enter your personal phone number that is verified by your Twilio account here."


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = TWILIO_ACC_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.sender_phone_no = TWILIO_PHONE_NO
        self.receiver_phone_no = VERIFIED_PHONE_NO

    def send_message(self, price, dep_city, dep_airport, arrival_city, arrival_airport, outbound_date, inbound_date):
        client = Client(self.account_sid, self.auth_token)

        client.messages \
            .create(
                body=f"Low price alert! Only S${price} to fly from "
                     f"{dep_city}-{dep_airport} to "
                     f"{arrival_city}-{arrival_airport}, from "
                     f"{outbound_date} to "
                     f"{inbound_date}.",
                from_=self.sender_phone_no,
                to=self.receiver_phone_no
            )
