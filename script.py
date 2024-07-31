# Do I need this? https://pypi.org/project/pyperclip/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

LOGIN_TIME = 20

browser = webdriver.Chrome()

browser.get('https://virginia.zoom.us/signin')

time.sleep(LOGIN_TIME)

browser.get('https://virginia.zoom.us/recording')

share_btns = browser.find_elements(By.CLASS_NAME, 'zm-button__slot')
share_btns = [b for b in share_btns if 'Share' in b.text]

for share_btn in share_btns:
    share_btn.click()
    share_link_text = browser.find_element(By.CLASS_NAME, 'share-link').text
    browser.find_element(By.CLASS_NAME, 'zm-dialog__close').click()

next_page_btn = browser.find_element(By.CLASS_NAME, 'zm-icon-right')

import pdb
pdb.set_trace()

# elem = browser.find_element(By.NAME, 'p')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)

# browser.quit()