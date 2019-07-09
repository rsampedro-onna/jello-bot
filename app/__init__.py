from flask import Flask

app = Flask(__name__)
app.config.from_object(f'app.config.{app.env}')

from app.slackbot import blueprint as slack_bot

app.register_blueprint(slack_bot, url_prefix='/slack')