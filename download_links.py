from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import selenium
import time

INFILENAME = 'link_texts.txt'

def parse_link_line(line):
    line = line.strip()
    link, _, password = line.split()
    return link, password

LOGIN_TIME = 20
MED_WAIT_TIME = 5
LONG_WAIT_TIME = 20
SMALL_WAIT_TIME = .5

browser = webdriver.Chrome()

with open(INFILENAME) as infile:
    for line in infile:
        link, password = parse_link_line(line)
        browser.get(link)
        time.sleep(MED_WAIT_TIME)

        pass_input = browser.find_element(By.ID, "passcode")
        pass_input.send_keys(password)
        button = browser.find_element(By.ID, "passcode_btn")
        button.click()
        
        time.sleep(MED_WAIT_TIME)
        download_btn = browser.find_element(By.CLASS_NAME, 'download-btn')
        download_btn.click()
        time.sleep(LONG_WAIT_TIME)

time.sleep(86400)