from json import loads, dumps
# from .psql_db import Distros
from datetime import datetime

class DevData(object):
	"""
	Class for representing the dev portifolio
	"""

#	user_id: str # user id
#	distro: str
#	fav_langs: list
#	github_link: str
#	custom_url: str
# avatar_distro_path (comming up soon)

	def __init__(self, poll):
		"""
		Class constructor, can be constructed using Dicts or Strings
		"""
		if type(poll) is str:
			poll = loads(poll)
		elif type(poll) is dict:
			self.user_id = poll["UserID"]
			self.distro  = poll["Distro"]
			self.fav_langs = poll["FavLangs"]
			self.github_link = poll["Github"]
			self.custom_link = poll["CustomURL"]
		elif type(poll) is tuple:
			self.user_id, self.distro, self.fav_langs, self.github_link, self.custom_link = poll
		else:
			self.user_id     = 0
			self.distro      = ""
			self.fav_langs   = []
			self.github_link = ""
			self.custom_link = ""
		# raise TypeError("Invalid type for converting the DevData object")
	
	def __dict__(self) -> dict: 
		return {
			"UserID": self.user_id,
			"Distro": self.distro,
			"FavLangs": self.fav_langs,
			"Github": self.github_link,
			"CustomURL": self.custom_link
		}
	
	def __tuple__(self) -> tuple:
		return (self.user_id, self.distro, self.fav_langs, self.github_link, self.custom_link, )

	def __str__(self) -> str:
		return dumps(self.__dict__())
	
	def __message__(self) -> str:
		nfav = ", ".join(self.fav_langs)
		return f"""
		>>> <@{self.user_id}> Portifolio and schizo data
Distro: {self.distro}
Favorite Languages: {nfav}
Github: {self.github_link}
Custom URL: {self.custom_link}
		"""

class Coordinate(object):
	"""
	Represents the minecraft coordinates data of a message or a database content.
	"""
	save_name = ""
	user_id = 0
	x_val = 0
	y_val = 0
	z_val = 0


	def __init__(self, args):
		"""
		Class constructor, starts the class using some values from args
		arg[0] => user_id, 
		arg[1] => save_name,
		arg[2] => X
		arg[3] => Y
		arg[4] => Z
		""" 
		if type(args) is str:
			self.user_id, self.save_name, self.x_val, self.y_val, self.z_val = args.split(" ")
		else:
			self.user_id, self.save_name, self.x_val, self.y_val, self.z_val = args

	
	def __tuple__(self) -> tuple:
		return self.user_id, self.save_name, self.x_val, self.y_val, self.z_val
	
	def __message__(self) -> str:
		return f"""
>>> {self.save_name} coordinates
X: {self.x_val} / Y: {self.y_val} / Z: {self.z_val}
		"""
	#TODO change to @property
	def coordinates(self) -> str:
		return f"X: {self.x_val} / Y: {self.y_val} / Z: {self.z_val}"

class SavedLink(object):
	"""
	Represents a link saved by the user in the database
	"""
	user_id = 0
	link_name = ""
	url = ""
	
	def __init__(self, args):
		"""
		Class constructor, starts the class using some values from args
		arg[0] => user_id, 
		arg[1] => save_name,
		arg[2] => URL
		"""
		if type(args) is tuple: 
			self.user_id, self.link_name, self.url = args
		elif type(args) is str:
			self.user_id, self.link_name, self.url = args.split(" ")
	
	def __tuple__(self) -> tuple:
		return self.user_id, self.link_name, self.url
	
	def __message__(self) -> str:
		return f"""
>>> Link ({self.link_name}): {self.url} """

class Coffee():
	"""
	Represents a coffee cups count record from the database table tb_coffee_counter
	"""

	def __init__(self, data):
		"""
		Class constructor
		data[0] => user id
		data[1] => total counts
		data[2] => last cup drinked
		"""
		if type(data) is str:
			self.user_id, self.total, self.last_cup = data.split(" ")
		else:
			self.user_id, self.total, self.last_cup = data
	
	def __tuple__(self) -> tuple:
		return self.user_id, self.total, self.last_cup
	
	def increase(self):
		self.last_cup = datetime.now()
		self.total += 1
	
	def decrease(self):  # DEBUG ONLY
		return self.total - 1 
	

