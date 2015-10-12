# -*- coding: utf-8 -*-
"""
    slackbot main
"""

import json

from slackbot import db, app, surveybot
from flask import render_template, flash, redirect, url_for, request, session, current_app

@app.route("/")
def home():
    """
        Home
    """
    return "Hi. This is the project: slackbot"

@app.route("/survey", methods=['POST'])
def survey():
    """
        Slack integration
    """
    # TODO auth check
    
    actions = {
        "list" : surveybot.listsurveys,
        "listall" : surveybot.listallsurveys,
        "this" : surveybot.createsurvey,
        "cancel" : surveybot.cancelsurvey,
        "close" : surveybot.closesurvey,
        "reply" : surveybot.vote,
        "myreply" : surveybot.myvote,
        "show" : surveybot.showresults,
        "publish" : surveybot.publishresults
    }

    app.logger.debug("request %s " % request.values)

    user_name = request.form['user_name']
    app.logger.debug("user_name: %s " % user_name)


    action_text = request.form['text']
    if action_text:
        action = action_text.split()[0]
        app.logger.debug("action: %s " % action)
        func = actions.get(action)
        if func is None:
            return "%s WTF?! Are you sure %s? You should choose an action between these ones : %s " % (action, user_name, actions.keys())
        return func(user_name, action_text)

    return "Hi %s, you should choose an action %s " % (user_name, actions.keys())
