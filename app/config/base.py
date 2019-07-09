import logging
import os

project_name = "Jello-Bot"

DEBUG = True

cwd = os.getcwd()

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

JELLO_CHANNEL = "#techathon-jellobot"

# LOGGING
LOGGER_NAME = "%s_log" % project_name
LOG_FILENAME = "/var/tmp/app.%s.log" % project_name
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)s\t: %(message)s"  # used by logging.Formatter
