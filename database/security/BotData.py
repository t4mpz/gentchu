from json import loads, dumps


class BotData(object):
	"""
	Simple class created to manage the sensitive bot data in the configurations file.
	"""

	CONFIG_PATH = "config/config.json"

	def __init__(self):
		"""
		Simple constructor
		"""

		with open(self.CONFIG_PATH, "r") as conf:
			self.content = loads(conf.read())
	
	@property
	def token(self) -> str:
		"""
		Returns the bot token (for GitHub security reasons)
		"""
		return self.content['bot']['token']
	
	@property
	def database_host(self) -> str:
		"""
		Returns the database host
		"""
		return self.content["database"]['host']
	
	@property
	def database_user(self) -> str:
		"""
		Returns the database username
		"""
		return self.content['database']['username']
	
	@property
	def database_pass(self) -> str:
		"""
		Returns the database password
		"""
		return self.content['database']['password']
	
	@property
	def db_name(self) -> str:
		"""
		Returns the database default name
		"""
		return self.content['database']['dbname']
	
	def get_content(self) -> dict:
		"""
		Just returns the configurations content
		"""
		return self.content
	

