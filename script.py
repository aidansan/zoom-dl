from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import selenium
import time

def scroll_click(elem, max_attempts=100000):
    for i in range(max_attempts):
        try:
            elem.click()
            return
        except selenium.common.exceptions.ElementClickInterceptedException:
            ActionChains(browser).scroll_by_amount(0, 10).perform()

LOGIN_TIME = 20
MED_WAIT_TIME = 5
SMALL_WAIT_TIME = .5

browser = webdriver.Chrome()

browser.get('https://virginia.zoom.us/signin')

time.sleep(LOGIN_TIME)

browser.get('https://virginia.zoom.us/recording')

time.sleep(MED_WAIT_TIME)

share_link_texts = []
while True:
    share_btns = browser.find_elements(By.CLASS_NAME, 'zm-button__slot')
    share_btns = [b for b in share_btns if 'Share' in b.text]

    for share_btn in share_btns:
        scroll_click(share_btn)
        time.sleep(SMALL_WAIT_TIME)
        share_link_text = browser.find_element(By.CLASS_NAME, 'share-link').text
        share_link_texts.append(share_link_text)
        browser.find_element(By.CLASS_NAME, 'zm-dialog__close').click()
        time.sleep(SMALL_WAIT_TIME)

    next_page_btn = browser.find_element(By.CLASS_NAME, 'btn-next')
    if next_page_btn.is_enabled():
        scroll_click(next_page_btn)
        time.sleep(SMALL_WAIT_TIME)
        browser.execute_script("window.scrollTo(0, document.body.scrollTop);")
    else:
        break