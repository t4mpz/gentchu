# import sys
# from os import path, listdir
from re import sub, findall
from database.psql_db import Distros
from bs4 import BeautifulSoup as BS
from requests import get

rr = get("https://fatduck.org/gnulinux/distro-logos.en.html")
bc = rr.content

# rr.close()

pc = BS(bc)
dc = Distros()

for img in pc.findAll("img"):
	dc.add_distro(img["alt"], "https://fatduck.org/" + img['src'])
		print("Added " + img['alt'])
