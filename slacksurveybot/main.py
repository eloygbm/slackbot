# -*- coding: utf-8 -*-
"""
    slacksurveybot main
"""

import json

from slacksurveybot import db, app
from flask import render_template, flash, redirect, url_for, request, session, current_app

@app.route("/")
def home():
    """
        Home
    """
    return "Hi. This is the project: slacksurveybot"

@app.route("/slack", methods=['POST'])
def slack():
    """
        Slack integration
    """
    # TODO auth check
    
    actions = {
        "list" : listsurveys,
        "add" : createsurvey
    }
    HELP_TEXT = "You shoud choose an action %s " % actions.keys()

    app.logger.debug("request %s " % request.values)

    user_name = request.form['user_name']
    app.logger.debug("user_name: %s " % user_name)


    action_text = request.form['text']
    if action_text:
        action = action_text.split()[0]
        app.logger.debug("action: %s " % action)
        func = actions.get(action)
        return func(user_name, action_text)

    return HELP_TEXT

def createsurvey(author, action_text):
    """
        Create a new survey
    """

    question = ""
    options = ""

    try:
        parameters = action_text.split(' ',1)[1]
        question = parameters.split()[0]
        options = parameters.split()[1]
        app.logger.debug("%s %s %s " % (author, question, options))

        database = db.get_db()
        database.execute('insert into survey (question, author, options) values (?, ?, ?)', [question, author, options])
        database.commit()

    except Exception, e:
        return('Parameters ERROR')   
    finally:
        database.close()    

    return "Hi %s the survey %s has been created." % (author, question)

def listsurveys(user_name, action_text):
    """
        List the surveys
    """

    database = db.get_db()
    cur = database.execute('SELECT id, question, author, options FROM survey')
    surveys = cur.fetchall()
    count_surveys = len(surveys)
    list_msg = "Hi %s, there are %i surveys. \n This is the list:" % (user_name, count_surveys)
    for row in surveys:
        list_msg = list_msg + "\n :small_blue_diamond: *%s* %s %s" % (row[0], row[1], row[3])
    return list_msg