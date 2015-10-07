# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

### Builtin configuration ###
DEBUG = True
SECRET_KEY = "$5$K8OLRBclmdsSWkFe$c65ae5RExEN86xTJous20UxU3gpZenqUf.3c3yPzV76"
SERVER_NAME = "localhost:5000"
### Database ###
DATABASE = join(_cwd, 'db/slacksurveybot.db')

