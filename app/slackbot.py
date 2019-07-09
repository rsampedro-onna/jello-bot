import json
import slack
import random
import logging

from flask import Blueprint, request, make_response, current_app

client = None

blueprint = Blueprint('slackbot', __name__)

JELLO_PATH = 'jello_json'

with open(f'{JELLO_PATH}/default.json') as f:
    default_jellos = json.load(f)


@blueprint.record
def record(setup_state):
    global client

    config = setup_state.app.config
    token = config.get('SLACK_BOT_TOKEN')

    if not token:
        raise Exception("SLACK_BOT_TOKEN not provided")

    client = slack.WebClient(token=token)


@blueprint.route('', methods=['GET'])
def root():
    make_response("Slack bot successfully initiated!")


@blueprint.route('/commands', methods=['POST'])
def commands():
    COMMAND_TABLE = {
        "/jello": jello
    }
    data = request.form
    command = data.get('command')
    func_to_call = COMMAND_TABLE.get(command)

    result = make_response("Command not implemented", 200)
    if func_to_call:
        result = func_to_call(data)

    return result


def jello(data):
    user_id = data.get("user_id")
    input_text = data.get('text', None)

    logging.debug(f"Jelloing user with id ({user_id}) with text \"{input_text}\"")

    user = client.users_info(
        user=user_id
    ).get("user")

    author = None

    if input_text != '':
        first_word = input_text.split()[0]
        if first_word.startswith("@"):
            author = first_word

    # Internal message
    internal_text = "You've just been Jelloed"
    if author:
        internal_text += f" by {author}"

    internal_json = {
        "replace_original": "true",
        "response_type": "ephemeral",
        "as_user": "true",
        "text": f"{internal_text}!!"
    }
    # Send jello Message
    __send_jello(user, user_id)

    return make_response(internal_json, 200)


def __send_jello(user, user_id):
    destination_channel = current_app.config.get('JELLO_CHANNEL')
    # External message
    try:
        with open(f'{JELLO_PATH}/{user_id}.json') as f:
            custom_jello = json.load(f)
    except Exception as e:
        custom_jello = None

    jello_data = None
    if custom_jello:
        jello_data = __get_random_jello_data(custom_jello)
    else:
        jello_data = __get_random_jello_data(default_jellos)

    if jello_data.get("text"):
        client.chat_postMessage(
            channel=destination_channel,
            as_user="false",
            username=user["profile"]["display_name"] or user["profile"]["real_name"] or "Missing Username",
            icon_url=user["profile"]["image_original"],
            text=jello_data.get("text"))

    if jello_data.get("blocks"):
        client.chat_postMessage(
            channel=destination_channel,
            as_user="false",
            username=user["profile"]["display_name"] or user["profile"]["real_name"] or "Missing Username",
            icon_url=user["profile"]["image_original"],
            text=jello_data.get("blocks"))


def __get_random_jello_data(jello_list):
    max = len(jello_list.get("jello"))
    index = random.randint(0, max - 1)
    logging.debug(f"jello {index} out of {max}")
    return jello_list.get('jello')[index]
