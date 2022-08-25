from psycopg2 import connect as psql
from .objects import *
from typing import List, Tuple
from .security.BotData import BotData
import logging

gbd = BotData()

class Database(object):
	
	connected  = False

	
	def __init__(self):
		self.connection = psql(
			host=gbd.database_host,
			database=gbd.db_name,
			user=gbd.database_user,
			password=gbd.database_pass
		)
		self.connected = True
		logging.basicConfig(filename="logs/database.log", format="%(asctime)s %(message)s", filemode="w")
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.DEBUG)
		self.logger.info(f"Started connection with database ({gbd.database_host}) OK")



class Distros(Database):
	"""
	Internal class used to access the distros data
	"""

	class InvalidDistro(BaseException):
		"""
		Represents the exception when a distro is not found
		"""

	class DistroExistsError(BaseException):
		"""
		Represents the warning/error for trying to add a already existing distro in the database
		"""

	def check_distro_exists(self, distro: str) -> bool:
		with self.connection.cursor() as cur:
			cur.execute("SELECT COUNT(*) FROM tb_distros WHERE LOWER(distro) = LOWER(%s);", (distro, ))
			return cur.fetchone()[0] > 0
	
	def get_distros(self):
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_distros;")
			c = cur.fetchall()
		return c
	
	def add_distro(self, distro: str, path: str = None):
		if not self.check_distro_exists(distro):
			with self.connection.cursor() as cur:
				cur.execute("INSERT INTO tb_distros (distro, img_path) VALUES (%s, %s);", (distro, path))
				self.connection.commit()
	
	def get_distro_url(self, distro: str) -> str:
		if self.check_distro_exists(distro):
			with self.connection.cursor() as cur:
				cur.execute("SELECT img_path FROM tb_distros WHERE LOWER(distro) = LOWER(%s);", (distro, ))
				return cur.fetchone()[0]
		else: return "https://pics.me.me/the-one-im-using-my-favorite-de-edition-19177604.png"   # default image when linux not found

	

class Portifolios(Database):
	"""
	Internal class to manage the portifolios table
	"""

	class PortifolioNotFound(BaseException):
		"""
		Exception for when a requested portifolio don't exist
		"""

	class PortifolioExistsError(BaseException):
		"""
		Exception for trying to insert duplicated userId in the database
		"""

	def check_userid(self, user_id) -> bool:
		n = False
		with self.connection.cursor() as cur:
			cur.execute("SELECT COUNT(*) FROM tb_portifolios WHERE user_id = %s", (user_id, ))
			n = cur.fetchone()[0] > 0
		return n
	
	def add_portifolio(self, devdata: DevData):
		"""
		Adds a new portifolio to the database
		"""
		if not self.check_userid(devdata.user_id):
			with self.connection.cursor() as cur:
				cur.execute("INSERT INTO tb_portifolios (user_id, distro, langs, github_link, custom_link) VALUES (%s, %s, %s, %s, %s)", devdata.__tuple__(), )
				self.connection.commit()
				self.logger.info(f"Inserted portifolio data for user {devdata.user_id}")
	
	def update_portifolio(self, new_data: DevData):
		"""
		Updates a portifolio on the database using the user_id
		"""
		if self.check_userid(new_data.user_id):
			with self.connection.cursor() as cur:
				cur.execute(
				"UPDATE tb_portifolios SET distro = %(Distro)s, langs=%(FavLangs)s, github_link = %(Github)s, custom_link = %(CustomURL)s WHERE user_id = %(UserID)s;",
				new_data.__dict__()
				)
				self.connection.commit()
				

	def del_portifolio(self, user_id: int):
		"""
		Removes a portifolio from the database
		"""
		if self.check_userid(user_id):
			with self.connection.cursor() as cur:
				cur.execute("DELETE FROM tb_portifolios WHERE user_id = %(id)s;", {"id": user_id})
				self.connection.commit()
	
	def get_portifolio(self, user_id: int) -> DevData:
		"""
		Gets a specific user portifolio
		"""
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_portifolios WHERE user_id = %(id)s;", {"id": user_id})
			ll = DevData(cur.fetchone())
		return ll
	
	def ls_portifolios(self):  # -> List[DevData]
		"""
		Lists all the portifolios
		"""
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_portifolios;")
			ll = [DevData(x) for x in cur.fetchall()]
		return ll

class CursedUsers(Database):
	"""
	Manages the Cursed Users database, to remove every message for spefic users, that con only be added by the server creator
	or by the bot creator
	"""
	creator_name = "tampinha#5789"
	creator_id   = 986681071565430804

	class InvalidMessageAuthor(BaseException):
		"""
		Raised when the command's message author isn't the creator (me >w<)
		"""
	
	class UserNotCursed(BaseException):
		"""
		Raised when the referred user isn't cursed
		"""
	
	class UserAlreadyCursed(BaseException):
		"""
		Raised when the referred user is already cursed in the database
		"""

	def check_author(self, author_id: int) -> bool:
		"""
		"""
		return self.creator_id == author_id

	def is_cursed(self, u: id) -> bool:
		"""
		Checks if a specific user is on the lists or not
		"""
		with self.connection.cursor() as cur:
			cur.execute("SELECT COUNT(*) FROM tb_cursed_users WHERE user_id = %s;", (u, ))
			return cur.fetchone()[0] > 0
	
	def add_cursed(self, to_curse: int):
		"""
		Adds a cursed user if the manager is the bot creator
		"""
		# if(manager_id != creator_id) raise self.InvalidManager("")
		#else:
		with self.connection.cursor() as cur:
			cur.execute("INSERT INTO tb_cursed_users (user_id) VALUES (%s);", (to_curse, ))
			self.connection.commit()
	
	def del_cursed(self, to_uncurse: int):
		"""
		Removes a user from the cursed list, uncursing him
		"""
		with self.connection.cursor() as cur:
			cur.execute("DELETE FROM tb_cursed_users WHERE user_id = %s;", (to_uncurse, ))
			self.connection.commit()
	
	def list_users(self):
		"""

		"""
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_cursed_users;")
			return cur.fetchall()


class MinecraftCoordinates(Database):
	"""
	Manages the minecraft coordinates database 
	"""

	# __LIMIT_USER = 5 # coordinates limits per user

	class CoordinateNotFound(BaseException):
		"""
		Raised when the referred coordinate name of a specific userID don't exist in the database
		"""
	
	class CoordinateExistsError(BaseException):
		"""
		Raised when the referred coordinate name of a specific user already exists in the database
		"""

	def get_user_coordinates(self, user_id: int):
		"""
		Returns all the coordinates that a user has
		"""
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_coordinates_mc WHERE user_id = %s;", (user_id, ))
			return [Coordinate(i) for i in cur.fetchall()]

	def get_coordinate(self, coordinate_name: str, user_id: int):
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_coordinates_mc WHERE save_name = %s AND user_id = %s ;", (coordinate_name, user_id))
			return Coordinate(cur.fetchone())
	
	def check_exists(self, coordinate_name: str, user_id: int) -> bool:
		with self.connection.cursor() as cur:
			cur.execute("SELECT COUNT(*) FROM tb_coordinates_mc WHERE user_id = %s AND save_name = %s;", (user_id, coordinate_name))
			return cur.fetchone()[0] > 0

	
	def add_coordinate(self, c: Coordinate):
		if not self.check_exists(c.save_name, c.user_id):
			with self.connection.cursor() as cur:
				cur.execute("INSERT INTO tb_coordinates_mc (user_id, save_name, x_val, y_val, z_val) VALUES (%s, %s, %s, %s, %s);", c.__tuple__())
				self.connection.commit()
	
	def del_coordinate(self, coord: Coordinate):
		if self.check_exists(coord.save_name, coord.user_id):
			with self.connection.cursor() as cur:
				cur.execute("DELETE FROM tb_coordinates_mc WHERE save_name = %s AND user_id = %s;", (coord.save_name, coord.user_id))
				self.connection.commit()
	
	def upd_coordinate(self, coord: Coordinate):
		if self.check_exists(coord.save_name, coord.user_id):
			with self.connection.cursor() as cur:
				cur.execute("UPDATE tb_coordinates_mc set x_val = %s, y_val = %s, z_val = %s WHERE save_name = %s AND user_id = %s;", 
				            (coord.x_val, coord.y_val, coord.z_val, coord.save_name, coord.user_id)
				)
				self.connection.commit()


class SavedLinks(Database):
	"""
	Manages the saved by user links table, these links exist in every server with the bot and the user
	"""

	class LinkNotFound(BaseException):
		"""
		Raised when a specified link save name and user id aren't the database, and can't be found 
		"""
	
	class LinkExistsError(BaseException):
		"""
		Raised when the specified link already exists in the database
		"""

	def check_exists(self, link_name: str, user_id: int) -> bool:
		with self.connection.cursor() as cur:
			cur.execute("SELECT COUNT(*) FROM tb_links WHERE user_id = %s AND link_name = %s;", (user_id, link_name))
			return cur.fetchone()[0] > 0


	def get_link(self, link_name: str, user_id: int) -> SavedLink:
		if self.check_exists(link_name, user_id):
			with self.connection.cursor() as cur:
				cur.execute("SELECT * FROM tb_links WHERE user_id = %s AND link_name = %s;", (user_id, link_name))
				return SavedLink(cur.fetchone())
	
	def get_user_links(self, user_id: int):
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_links WHERE user_id = %s;", (user_id, ))
			return [SavedLink(x) for x in cur.fetchall()]
	
	def add_link(self, link: SavedLink):
		if not self.check_exists(link.link_name, link.user_id):
			with self.connection.cursor() as cur:
				cur.execute("INSERT INTO tb_links (user_id, link_name, url) VALUES (%s, %s, %s);", link.__tuple__())
				self.connection.commit()
	
	def del_link(self, link: SavedLink):
		if self.check_exists(link.link_name, link.user_id):
			with self.connection.cursor() as cur:
				cur.execute("DELETE FROM tb_links WHERE user_id = %s AND link_name = %s;", (link.user_id, link.link_name))
				self.connection.commit()
	
	def upd_link(self, link: SavedLink):
		if self.check_exists(link.link_name, link.user_id):
			with self.connection.cursor() as cur:
				cur.execute("UPDATE tb_links SET url = %s WHERE user_id = %s AND link_name = %s;", (link.url, link.user_id, link.link_name))
				self.connection.commit()
	
class CoffeeCounter(Database):
	"""
	Manages the coffee counters table in the database
	"""

	class CounterNotExists(BaseException):
		"""
		Raised when the database don't have a counter record for the specified user
		"""

	def check_counting(self, user_id: int) -> bool:
		with self.connection.cursor() as cur:
			cur.execute("SELECT COUNT(*) FROM tb_coffee_counter WHERE user_id = %s;", (user_id, ))
			return cur.fetchone()[0] > 0
	
	def get_counter(self, user_id: int) -> Coffee:
		with self.connection.cursor() as cur:
			cur.execute("SELECT * FROM tb_coffee_counter WHERE user_id = %s;", (user_id, ))
			return Coffee(cur.fetchone())
	
	def add_counter(self, user_id: int):
		"""
		Creates the counter log in the database for a user if the log don't exists, starting at the first cup.
		If the log exists, then it will just increment the counter 
		"""
		with self.connection.cursor() as cur:
			if not self.check_counting(user_id):
				cur.execute("INSERT INTO tb_coffee_counter (user_id) VALUES (%s);", (user_id, ))
			else:
				c = self.get_counter(user_id)
				c.increase()
				cur.execute("UPDATE tb_coffee_counter set total = %s, last_cup = %s WHERE user_id = %s;", (c.total, c.last_cup, c.user_id))
			self.connection.commit()
	
	def del_counter(self, user_id: int):
		if self.check_counting(user_id):
			with self.connection.cursor() as cur:
				cur.execute("DELETE FROM tb_coffee_counter WHERE user_id = %s;", (user_id, ))
				self.connection.commit()


