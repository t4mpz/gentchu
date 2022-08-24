from selenium import webdriver
from selenium.webdriver.common.by import By
from requests import get
from urllib.request import urlretrieve
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def download_from_twitter(twit, path):
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")
	wbd = webdriver.Chrome("/usr/lib/chromium/chromedriver", chrome_options=options)
	waiter = WebDriverWait(wbd, 10)
	wbd.get("https://pt.savefrom.net/97/download-from-twitter")
	inp = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#sf_url")))
	inp.send_keys(twit, Keys.RETURN)
	try:
		dw_button= waiter.until(
			EC.presence_of_element_located((By.CLASS_NAME, "link-download"))
		)
	finally:
		# dw_button.click()
		vd_name = dw_button.get_attribute("download").replace(" ", "_")
		vd_url = dw_button.get_attribute("href")
		print(vd_url)
		# urlretrieve(vd_url, "tmp/test.mp4")
		rr = get(vd_url, timeout=10, stream=True)
		with open(path, "wb") as st:
		 	 for chunk in rr.iter_content(1024 * 1024): st.write(chunk)
