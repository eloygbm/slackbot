# -*- coding: utf-8 -*-
"""
    Data Base management
"""

import sqlite3
import os
from slackbot import app
from flask import _app_ctx_stack


def init_db():
    """Creates the database tables."""
    with app.app_context():
        database = get_db()
        with app.open_resource("scripts/schema.sql", mode="r") as sql_file:
            database.cursor().executescript(sql_file.read())
        database.commit()

def get_db():
    """
        Opens a new database connection if there is none
        yet for the current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        app.logger.debug("DB not in the app ctx stack")
        sqlite_db = sqlite3.connect(os.path.join(app.instance_path, \
        	app.config['DATABASE']))
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db
