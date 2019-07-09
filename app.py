import slack
import os
import json

import requests
from flask import Flask, request, make_response, Response

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

client = slack.WebClient(token=SLACK_BOT_TOKEN)

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
    print (data)
    jello_json = {
        "replace_original": "true",
        "response_type": "ephemeral",
        "as_user": "false",
        "username": data.get("user_name"),
        "text": "ecto1"
        # "text": "Thanks for your request, we'll process it and get back to you."
    }
    alt = {
        "text": "Would you like to play a game?",
        "attachments": [
            {
                "text": "Choose a game to play",
                "fallback": "You are unable to choose a game",
                "callback_id": "wopr_game",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "game",
                        "text": "Chess",
                        "type": "button",
                        "value": "chess"
                    },
                    {
                        "name": "game",
                        "text": "Falken's Maze",
                        "type": "button",
                        "value": "maze"
                    },
                    {
                        "name": "game",
                        "text": "Thermonuclear War",
                        "style": "danger",
                        "type": "button",
                        "value": "war",
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "Wouldn't you prefer a good game of chess?",
                            "ok_text": "Yes",
                            "dismiss_text": "No"
                        }
                    }
                ]
            }
        ]
    }
    # requests.post(url=data["response_url"], data=alt)
    user = client.users_info(
        user=data.get("user_name")
    )
    response = client.chat_postMessage(
        channel='#techathon-jellobot',
        as_user= "false",
        username= user["profile"]["display_name"] or user["profile"]["real_name"] or "Missing Username",
        image_url= user["profile"]["image_original"],
        text=data)
    print (response)
    return make_response(jello_json, 200)

@app.route("/slack/interactive", methods=["POST"])
def interactive():
    data = json.loads(request.form.to_dict()["payload"])
    print(data)
    # response = {
    #     "replace_original": "true",
    #     "response_type": "in_channel",
    #     "as_user": "false",
    #     "username": data["user_name"],
    #     "text": "Thanks for your request, we'll process it and get back to you."
    # }
    x = client.chat_update(channel=data["channel"]["id"],
                       ts=data["message_ts"],
                       text="Updated now")
                       #as_user=False,
                       #replace_original= True,
                       #username=data["user"]["name"])

    print (x)
    return make_response({}, 200)


if __name__ == '__main__':
    app.run("0.0.0.0")
