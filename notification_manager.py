import os
import smtplib
from twilio.rest import Client


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        # Retrieve environment variables only once
        self.smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["EMAIL_PASSWORD"]
        self.twilio_virtual_number = os.environ["TWILIO_VIRTUAL_NUMBER"]
        self.twilio_verified_number = os.environ["USER_NUMBER"]
        self.whatsapp_number = os.environ["TWILIO_WHATSAPP_NUMBER"]

        # Set up Twilio Client and SMTP connection
        self.client = Client(os.environ['TWILIO_SID'], os.environ["TWILIO_AUTH_TOKEN"])
        self.connection = smtplib.SMTP(os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"])


    def send_sms(self, message_body):
        """
            Sends an SMS message through the Twilio API.
            This function takes a message body as input and uses the Twilio API to send an SMS from
            a predefined virtual number (provided by Twilio) to your own "verified" number.
            It logs the unique SID (Session ID) of the message, which can be used to
            verify that the message was sent successfully.
            Parameters:
            message_body (str): The text content of the SMS message to be sent.
            Returns:
            None
            Notes:
            - Ensure that `TWILIO_VIRTUAL_NUMBER` and `TWILIO_VERIFIED_NUMBER` are correctly set up in
            your environment (.env file) and correspond with numbers registered and verified in your
            Twilio account.
            - The Twilio client (`self.client`) should be initialized and authenticated with your
            Twilio account credentials prior to using this function when the Notification Manager gets
            initialized.
        """
        message = self.client.messages.create(
            from_= os.environ["TWILIO_VIRTUAL_NUMBER"],
            body= message_body,
            to= os.environ["USER_NUMBER"]
        )

        print(message.sid)


    def send_whatsapp(self, message_body):
        message = self.client.messages.create(
            from_=f'whatsapp:{os.environ["TWILIO_WHATSAPP_NUMBER"]}',
            body=message_body,
            to=f'whatsapp:{os.environ["USER_NUMBER"]}'
        )


        print(message.sid)


    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.email, self.email_password)

            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject: New Low Price Flight! \n\n{email_body}".encode('utf-8')
                )