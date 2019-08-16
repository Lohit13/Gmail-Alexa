from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.utils import parsedate_tz
import datetime, dateutil.tz

from pprint import pprint

from app.models import Email

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def getDateObjFromDate(date):
	parsed_date = list(parsedate_tz(date))
	tzinfo = dateutil.tz.tzoffset(None, parsed_date[-1])
	return datetime.datetime(parsed_date[0], parsed_date[1], parsed_date[2], parsed_date[3], parsed_date[4], parsed_date[5]).replace(tzinfo=tzinfo)

def getEmails(gte, lte):
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('/Users/b0206610/Desktop/Gmail-Alexa/app/credentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('gmail', 'v1', http=creds.authorize(Http()))

	query = "before: {0} after: {1}".format(lte.strftime('%Y/%m/%d'),gte.strftime('%Y/%m/%d'))

	batch = service.users().messages().list(userId='me', q=query,labelIds = ['INBOX', 'UNREAD']).execute()

	emails = []
	
	for message in batch['messages']:
		msg = service.users().messages().get(userId='me', id=message['id']).execute()
		date = datetime.datetime.fromtimestamp(int(msg['internalDate'])/1000)
		if date >= gte and date <= lte:
			sender = list(filter(lambda x: x['name'] == 'From', msg['payload']['headers']))[0]['value']
			receiver = list(filter(lambda x: x['name'] == 'To', msg['payload']['headers']))[0]['value']
			try:
				timestamp = getDateObjFromDate(list(filter(lambda x: x['name'] == 'Date', msg['payload']['headers']))[0]['value'])
			except Exception as e:
				timestamp = None
			subject = list(filter(lambda x: x['name'] == 'Subject', msg['payload']['headers']))[0]['value']
			snippet = msg['snippet']
			emails.append(Email(sender, receiver, timestamp, subject, snippet))
		else:
			break

	return emails
				
def main():
	today = datetime.date.today()
	gte = datetime.datetime(today.year, today.month, today.day)
	lte = gte + datetime.timedelta(days=1)

	lte = datetime.datetime.now()
	gte = gte - datetime.timedelta(days=5)

	getEmails(gte, lte)

if __name__=='__main__':
	main()
