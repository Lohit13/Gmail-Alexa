class Email(object):
	def __init__(self, sender, receiver, timestamp, subject, snippet):
		self.sender = sender
		self.receiver = receiver
		self.timestamp = timestamp
		self.subject = subject
		self.snippet = snippet

	def getSender(self):
		return self.sender

	def getTimestamp(self):
		return self.timestamp

	def getSubject(self):
		return self.subject

	def getSnippet(self):
		return self.snippet

	def __repr__(self):
		output = "From : " + self.sender + '\n'
		output += "To : " + self.receiver + '\n'
		output += "Date : " + str(self.timestamp) + '\n'
		output += "Snippet : " + self.snippet
		return output

	def __str__(self):
		output = "From : " + self.sender + '\n'
		output += "To : " + self.receiver + '\n'
		output += "Date : " + str(self.timestamp) + '\n'
		output += "Snippet : " + self.snippet
		return output
	