from flask import Blueprint, request
import datetime

import app.gmail_access as gmail_access

gmail = Blueprint('auth', __name__, url_prefix='/gmail')

@gmail.route('/')
def hello_world():
	return 'Hello, World!'

@gmail.route('/fetchMails')
def fetch_mails():
	lte = datetime.datetime.now()
	gte = lte - datetime.timedelta(days=1)
	return gmail_access.getEmails(gte, lte)

