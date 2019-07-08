import slack
import os
from flask import Flask, request, make_response, Response

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

client = slack.WebClient(token="xoxb-13246082566-675986705106-93UhYcHOLvCDjd4CTmPyr5BT")

# Helper for verifying that requests came from Slack
def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
    return make_response("Request contains invalid Slack verification token", 403)

response = client.chat_postMessage(
    channel='#techathon-jellobot',
    blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Danny Torrence left the following review for your property:"
            }
        }
    ],
    as_user=True)

app = Flask(__name__)

assert response["ok"]
# assert response["message"]["text"] == "Hello world!"
