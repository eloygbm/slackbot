"""
  Manage app
"""
from slacksurveybot import db, app
from flask.ext.script import Manager

manager = Manager(app)

@manager.command
def init_db():
    """
        To initialize the DB
    """
    app.logger.debug("Init DB ...")
    db.init_db()

if __name__ == "__main__":
    manager.run()