import slack
import os
import json
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
    data = request.form["payload"]
    print (data)
    response = client.chat_postMessage(
        channel='#techathon-jellobot',
        text=data)
    return make_response(200)

@app.route("/slack/interactive", methods=["POST"])
def interactive():
    form_json = json.loads(request.form["payload"])
    print (form_json)
    return make_response(200)


if __name__ == '__main__':
    app.run("0.0.0.0")
