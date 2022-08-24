from json import loads, dumps
from typing import AnyStr
from .objects.devdata import DevData

class JSONDatabase(object):
	"""
	Uses the JSON base database, until the SQL database is ready
	"""

	content: dict = dict()
	lf: AnyStr

	def __init__(self, fl: AnyStr):
		"""
		Constructor, loads the JSON file
		"""
		with open(fl, "r+") as jsonf:
			content = loads(jsonf.read())
		self.lf = fl

	def commit(self):
		"""
		class destructor, writes the content before being torn into pieces
		"""
		with open(self.lf, "w") as jsonf:
			jsonf.write(dumps(self.content))
	
	def __str__(self) -> str: return dumps(self.content)

	# ======================================================================
	# DEVELOPER DATA METHODS SECTION 
	
	def check_exists_dd(self, user_id: int) -> bool:
		"""
		Checks if a dev data contents have a dev data specific about a id
		"""
		for dd in self.content["devdata"]:
			if dd["UserID"] == user_id:
				return True
		return False
	
	def add_devdata(self, devdata):
		"""
		Adds a new dev data object to the JSON database
		uses the devdata content as a object/instance of DevData class
		"""
		if not self.check_exists_dd(devdata.user_id):
			self.content["devdata"].append(dict(devdata))
	
	def del_devdata(self, user_id: int):
		"""
		Removes a portifolio from the database
		"""
		self.content["devdata"] = list(filter(lambda x: int(x["UserID"]) != user_id, self.content["devdata"]))
	
	def upd_devdata(self, user_id: int, new_data):
		"""
		Updates a portifolio with new data
		"""
		self.content["devdata"] = list(map(lambda x: dict(new_data) if x["UserID"] == user_id else x, self.content["devdata"]))
