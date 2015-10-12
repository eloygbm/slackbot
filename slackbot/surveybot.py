# -*- coding: utf-8 -*-
"""
    surveybot main
"""

import requests
import json
from slackbot import db, app

def vote (user, action_text):
    """
        Vote for a survey    
    """
    survey_id = ""
    option = ""

    try:
        parameters = action_text.split(' ',1)[1]
        survey_id = parameters.split(' ')[0]
        option = parameters.split(' ')[1]

        app.logger.debug("%s %s %s " % (user, survey_id, option))

    except Exception, e:
        return('Parameters ERROR - Example to vote option Green for survey #2: `/survey reply 2 Green`')

    try:
        database = db.get_db()
        cur = database.execute('select id, question, author from survey where id = ? and open is "true"', [survey_id])
        survey = cur.fetchone()
        if survey is None:
            return "No %s, the survey %s is closed! " % (user, survey_id)
        database.execute('delete from vote where survey_id = ? and user = ?', [survey_id, user])
        database.execute('insert into vote (survey_id, user, option) values (?, ?, ?)', [survey_id, user, option])
        database.commit()

    except Exception, e:
        app.logger.debug(e)
        return('DB ERROR')   
    finally:
        database.close()    

    return "Hi %s, you voted the survey %s with option %s." % (user, survey_id, option)

def myvote (user, action_text):
    """
        Show my vote for a survey    
    """
    survey_id = ""
    option = ""
    try:
        parameters = action_text.split(' ',1)[1]
        survey_id = parameters.split(' ')[0]

        app.logger.debug("%s %s" % (user, survey_id))

    except Exception, e:
        return('Parameters ERROR - Example to show your vote survey #2: `/survey myreply 2`')

    try:
        database = db.get_db()
        cur = database.execute('select option from vote where survey_id = ? and user = ?', [survey_id, user])
        option = cur.fetchone()
    except Exception, e:
        app.logger.debug(e)
        return('DB ERROR')   
    finally:
        database.close()    

    if option is None:
        return "Hi %s, you didn't vote the survey %s." % (user, survey_id)
    else:
        return "Hi %s, you voted the survey %s with option %s." % (user, survey_id, option[0][0])

def cancelsurvey(author, action_text):
    """
        Cancel a survey
    """

    survey_id = ""
    try:
        parameters = action_text.split(' ',1)[1]
        survey_id = parameters.split()[0]

        app.logger.debug("%s %s " % (author, survey_id))

    except Exception, e:
        return('Parameters ERROR - Example to cancel survey #2 : `/survey cancel 2`')

    try:
        database = db.get_db()
        cur = database.execute('select id, question, author from survey where id = ? and author = ?', [survey_id, author])
        survey = cur.fetchone()
        if survey is None:
            return "No no no no no %s, the survey %s is not yours :confused: " % (author, survey_id)
        database.execute('delete from survey where id = ? and author = ?', [survey_id, author])
        database.commit()

    except Exception, e:
        return('DB ERROR')   
    finally:
        database.close()    

    return "Hi %s, the survey %s has been canceled." % (author, survey_id)

def closesurvey(author, action_text):
    """
        Close a survey
    """

    survey_id = ""
    try:
        parameters = action_text.split(' ',1)[1]
        survey_id = parameters.split()[0]

        app.logger.debug("%s %s " % (author, survey_id))

    except Exception, e:
        return('Parameters ERROR - Example to close survey #2 : `/survey close 2`')

    try:
        database = db.get_db()
        cur = database.execute('select id, question, author from survey where id = ? and author = ?', [survey_id, author])
        survey = cur.fetchone()
        if survey is None:
            return "No no no no no %s, the survey %s is not yours :confused: " % (author, survey_id)
        database.execute('update survey set open = "false" where id = ? and author = ?', [survey_id, author])
        database.commit()

    except Exception, e:
        return('DB ERROR')   
    finally:
        database.close()    

    return "Hi %s, the survey %s has been closed." % (author, survey_id)

def createsurvey(author, action_text):
    """
        Create a new survey
    """

    question = ""
    options = ""
    warning_msg = ""
    try:
        parameters = action_text.split(' ',1)[1]
        question = parameters.split('options')[0]
        options = parameters.split('options')[1]

        if not ',' in options:
            warning_msg = ":warning: There are limited options"

        app.logger.debug("%s %s %s " % (author, question, options))

    except Exception, e:
        return('Parameters ERROR - Example to create new survey: `/survey this What colour is your favorite? options red, gree, blue`')

    try:
        database = db.get_db()
        database.execute('insert into survey (question, author, options) values (?, ?, ?)', [question, author, options])
        database.commit()
    except Exception, e:
        return('DB ERROR')
    finally:
        database.close()    

    return "Hi %s, the survey %s has been created. %s" % (author, question, warning_msg)

def listsurveys(user_name, action_text):
    """
        List the surveys
    """

    database = db.get_db()
    cur = database.execute('SELECT id, question, author, options, open FROM survey where open is "true"')
    surveys = cur.fetchall()
    count_surveys = len(surveys)
    list_msg = "Hi %s, there are %i surveys open. \n This is the list:" % (user_name, count_surveys)
    for row in surveys:
        list_msg = list_msg + "\n %s *%s* *%s* asks *%s*, the survey is *%s* and options are: *[%s]*" % (":clipboard:" if row[4]=='true' else ":x:", row[0], row[2], row[1], "open" if row[4]=='true' else "close", row[3])
    return list_msg

def listallsurveys(user_name, action_text):
    """
        List All the surveys. Including closed.
    """

    database = db.get_db()
    cur = database.execute('SELECT id, question, author, options, open FROM survey')
    surveys = cur.fetchall()
    count_surveys = len(surveys)
    list_msg = "Hi %s, there are %i surveys. \n This is the list:" % (user_name, count_surveys)
    for row in surveys:
        list_msg = list_msg + "\n %s *%s* *%s* asks *%s*, the survey is *%s* and options are: *[%s]*" % (":clipboard:" if row[4]=='true' else ":x:", row[0], row[2], row[1], "open" if row[4]=='true' else "close", row[3])
    return list_msg

def showresults(user_name, action_text):
    """
        Show results of a survey
    """

    survey_id = ""
    try:
        parameters = action_text.split(' ',1)[1]
        survey_id = parameters.split()[0]

        app.logger.debug("%s %s " % (user_name, survey_id))

    except Exception, e:
        return('Parameters ERROR - Example to show results for survey #2 : `/survey show 2`')

    database = db.get_db()
    survey_data = database.execute('SELECT s.id, s.question, s.author, s.options FROM survey s WHERE s.id = ?', [survey_id])
    try:
        survey_row = survey_data.next()
        list_msg = "Hi %s. \n *Survey:* %s - %s \n *Author:* %s \n *Options are:* %s \n *Results:*" % (user_name, survey_id, survey_row[1], survey_row[2], survey_row[3])
    except Exception, e:
        app.logger.debug(e)
        return "Hi %s. The survey %s does not exist." % (user_name, survey_id)

    cur = database.execute('SELECT v.option, count(v.option) as count FROM vote v WHERE v.survey_id = ? GROUP BY v.option ORDER BY count DESC' , [survey_id])
    
    try:
        first_row = cur.next()
        results = [first_row] + cur.fetchall()
        for row in results:
            list_msg = list_msg + "\n :small_blue_diamond: Option *%s* = %s votes" % (row[0], row[1])

        return list_msg
    except Exception, e:
        app.logger.debug(e)
        return list_msg + "\n There are no votes."


def publishresults(user_name, action_text):
    """
        Publish the results to a channel
    """
    URL_HOOK = "https://hooks.slack.com/services/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"
    survey_id = ""
    channel = ""
    try:
        parameters = action_text.split(' ',1)[1]
        survey_id = parameters.split(' ')[0]
        channel = parameters.split(' ')[1]

        app.logger.debug("%s %s %s" % (user_name, survey_id, channel))

    except Exception, e:
        return('Parameters ERROR - Example to publish results to #general channel for survey #2 : `/survey publish 2 #general`')

    results = showresults("everybody", action_text)

    payload = {"text": results, "channel": channel, "username": "%s says:" % user_name, "icon_emoji": ":clipboard:"}

    app.logger.debug(payload)
    response = requests.post(URL_HOOK, data=json.dumps(payload))
    
    app.logger.debug(response)

    return "Publish survey %s to %s done!" % (survey_id, channel)
