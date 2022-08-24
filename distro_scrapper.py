from selenium import webdriver
from bs4 import BeautifulSoup

search = "arch"
driver = webdriver.PhantomJS()
ss = driver.get("https://fatduck.org/gnulinux/distro-logos.en.html")
soup = BeautifulSoup(driver.page_source)
rs = soup.find("a", {"href": "http://distrowatch.com/" + search}).find("img")
print(rs)
	
