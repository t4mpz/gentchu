from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from typing import AnyStr
import discord
from bs4 import BeautifulSoup

class Distro(object):
	"""
	Class for representing a distro data 
	"""

	STATUS_ACTIVE       = 0
	STATUS_DISCONTINUED = 1
	STATUS_NONE         = -1

	def __init__(self, distro_name = "", popularity = 0, categories = [], status = -1, img_link = ""):
		"""
		Class constructor with the specified data
		"""
		self.distro_name = distro_name
		self.popularity = popularity
		self.categories = categories
		self.status = status
		self.img = img_link
	
	def appear(self):
		"""
		Returns the distro specified as it randomly appeared
		"""
		em = discord.Embed()
		cc = self.distro_name.capitalize()
		em.title(f"A wild distro appears. *{cc}* #_{self.popularity}_")
		em.set_thumbnail(url=self.img)
	
	def view(self):
		"""
		Returns the distro specified as a search for it occoured
		"""
		em = discord.Embed()
		em.title(f"*{self.distro_name}* #_{self.popularity}_")
		em.add_field("Distrowatch link", value="https://distrowatch.com/table.php?distribuition=" + self.distro_name)
		em.set_thumbnail(url=self.img)


class DistroWatch(object):
	"""
	A class to manage the operations with  the distrowatch web site
	"""

# Exceptions -------------------------------------------
# ------------------------------------------------------


	RANDOM_LINK = "https://distrowatch.com/random.php"
	# DISTRO_PAGE_LINK = ""


	@staticmethod
	def generate_distro_page_link(distro_name: str) -> str:
		return "https://distrowatch.com/table.php?distribution=" + distro_name

	def __init__(self):
		"""
		Simple constructor for the scrapper
		"""
		

	def get_random_distro(self):
		"""
		Goes to the random distro page and gets a random distro
		"""
		
		bs = BeautifulSoup(src)
		maintitle = bs.find("div", id_="TablesTitle")
		print(maintitle.find("h1").get_text)


if __name__ == "__main__":
	


