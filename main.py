from fastapi import FastAPI
from twilio.rest import Client
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv(dotenv_path=".env")

app = FastAPI()

class AlertMessage(BaseModel):
    phone_no: str
    message: str

@app.post("/send_alert_message")
def sendAlertMessage(alertMessage: AlertMessage):
    # example: phone_no=+910000000000 (country code +91)
    # example: message=xyz

    try:
        account_sid = os.getenv("ACCOUNT_SID")  
        auth_token = os.getenv("AUTH_TOKEN")
        twilio_phone_no = os.getenv("TWILIO_PHONE_NUMBER")

        twilioConnection = Client(account_sid, auth_token)

        msg = twilioConnection.messages.create(
            to=alertMessage.phone_no,
            from_=twilio_phone_no,
            body=alertMessage.message
        )
        return {"status": "Message Sent", "message_id": msg.sid}
    except Exception as e:
        return {"status": "Error", "message": str(e)}