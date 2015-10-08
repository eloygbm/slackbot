# -*- coding: utf-8 -*-
"""
	Init slackbot
"""

from flask import Flask
from logging import FileHandler
from logging import Formatter
import logging

app = Flask(__name__)
app.config.from_object("settings")
FILE_HANDLER = FileHandler('./logs/slackbot.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s ''[in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(FILE_HANDLER)

# import slackbot.surveybot
import slackbot.main
