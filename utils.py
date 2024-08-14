from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import selenium
import time
from datetime import date, datetime
import json
import os

PATH_TO_DOWNLOADS = "/Users/aidansan/Downloads"
ZOOM_URL = 'https://virginia.zoom.us'
START_DAY = "2024-06-17"
END_DAY = "2024-07-19"


LOGIN_TIME = 20
MED_WAIT_TIME = 5
SMALL_WAIT_TIME = .5
MAX_DOWNLOAD_TIME = 360






START_DAY = date.fromisoformat(START_DAY)
END_DAY = date.fromisoformat(END_DAY)

# Continuously scrolls a little bit until you are able to click the button
def scroll_click(elem, max_attempts=100000):
    for i in range(max_attempts):
        try:
            elem.click()
            return
        except selenium.common.exceptions.ElementClickInterceptedException:
            ActionChains(browser).scroll_by_amount(0, 10).perform()

# https://stackoverflow.com/questions/34338897/python-selenium-find-out-when-a-download-has-completed
# Checks the download folder if there is any file ending in .crdownload 
# and returns the newest created file in the download folder
def download_wait():
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < MAX_DOWNLOAD_TIME:
        time.sleep(1)
        dl_wait = False
        latest_file = None
        latest_filetime = 0
        for fname in os.listdir(PATH_TO_DOWNLOADS):
            if fname.endswith('.crdownload'):
                dl_wait = True
            else:
                cur_filetime = os.path.getctime(os.path.join(PATH_TO_DOWNLOADS, fname))
                if  cur_filetime > latest_filetime:
                    latest_filetime = cur_filetime
                    latest_file = fname
        seconds += 1
    return latest_file