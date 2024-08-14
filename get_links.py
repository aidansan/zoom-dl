from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import selenium
import time
from datetime import date, datetime
import json
import os
from utils import *

def get_detail_page_link_data(browser):
    # Goes to recordings Zoom page
    browser.get(f'{ZOOM_URL}/recording')
    time.sleep(MED_WAIT_TIME)

    link_data = []
    while True:
        # Goes through each row in the information table
        meeting_rows = browser.find_elements(By.CLASS_NAME, 'zm-table__row')
        for meeting_row in meeting_rows:
            cols = meeting_row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >=5:
                meeting_name = cols[1].text
                meeting_id = cols[2].text
                date_text = cols[3].text
                size_text = cols[4].text

                # Checks if the meeting happens between the start and end date
                day = datetime.strptime(date_text, '%b %d, %Y %I:%M %p').date()
                if START_DAY <= day <= END_DAY:
                    link = meeting_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    link_data.append([link, meeting_name, meeting_id, date_text, size_text])

        # Goes to the next page of links
        next_page_btn = browser.find_element(By.CLASS_NAME, 'btn-next')
        if next_page_btn.is_enabled():
            scroll_click(next_page_btn)
            time.sleep(SMALL_WAIT_TIME)
            browser.execute_script("window.scrollTo(0, document.body.scrollTop);")
        else:
            break
    return link_data

def main():
    browser = webdriver.Chrome()

    browser.get(f'{ZOOM_URL}/signin')
    time.sleep(LOGIN_TIME)

    link_data = get_detail_page_link_data(browser)
    with open('download_links.tsv', 'w') as outfile:
        for row in link_data:
            outfile.write('\t'.join(row) + '\n')

if __name__ == '__main__':
    main()