import slack
import os
import json

import requests
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

app = Flask(__name__)

@app.route("/")
def base():
    return make_response("Hello there")

@app.route("/slack/commands", methods=["POST"])
def commands():
    data = request.form
    print(json.dumps(request, indent=4))
    print (data)
    jello_json = {
        "replace_original": "true",
        "response_type": "in_channel",
        "as_user": "false",
        "username": data["user_name"],
        "blocks":[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "A message *with some bold text* and _some italicized text_."
                }
            }
        ],
        # "text": "Thanks for your request, we'll process it and get back to you."
    }
    alt = {
    }
    requests.post(url=data["response_url"], data=jello_json)
    # response = client.chat_postMessage(
    #     channel='#techathon-jellobot',
    #     text=data)
    return make_response(jello_json, 200)

@app.route("/slack/interactive", methods=["POST"])
def interactive():
    data = request.form
    print(data)
    return make_response({}, 200)


if __name__ == '__main__':
    app.run("0.0.0.0")
