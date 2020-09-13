class User:
	def __init__(self, username, name, chats, number):
		self.username = username
		self.name = name
		self.chats = chats
		self.number = number
	
	@property
	def Name(self):
		return self.name

	@property
	def Username(self):
		return self.username

	@property
	def Number(self):
		return self.number