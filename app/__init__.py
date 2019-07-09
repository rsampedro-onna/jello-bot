from flask import Flask
import logging, sys, os

app = Flask(__name__)
app.config.from_object(f'app.config.{app.env}')
app.debug = app.config.get("DEBUG")

if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))



from app.slackbot import blueprint as slack_bot

app.register_blueprint(slack_bot, url_prefix='/slack')