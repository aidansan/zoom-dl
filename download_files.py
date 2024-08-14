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

def scroll_click(elem, max_attempts=100000):
    for i in range(max_attempts):
        try:
            elem.click()
            return
        except selenium.common.exceptions.ElementClickInterceptedException:
            ActionChains(browser).scroll_by_amount(0, 10).perform()

# https://stackoverflow.com/questions/34338897/python-selenium-find-out-when-a-download-has-completed
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

def get_detail_page_links(browser):
    detail_links = []
    while True:
        meeting_rows = browser.find_elements(By.CLASS_NAME, 'zm-table__row')
        for meeting_row in meeting_rows:
            cols = meeting_row.find_elements(By.TAG_NAME, 'td')
            if len(cols) == 7:
                date_text = cols[3].text
                day = datetime.strptime(date_text, '%b %d, %Y %I:%M %p').date()

                if START_DAY <= day <= END_DAY:
                    link = meeting_row.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    detail_links.append(link)

        next_page_btn = browser.find_element(By.CLASS_NAME, 'btn-next')
        if next_page_btn.is_enabled():
            scroll_click(next_page_btn)
            time.sleep(SMALL_WAIT_TIME)
            browser.execute_script("window.scrollTo(0, document.body.scrollTop);")
        else:
            break
    return detail_links

def download_files(browser, detail_link):
    browser.get(detail_link)
    time.sleep(MED_WAIT_TIME)

    links_div = browser.find_element(By.CLASS_NAME, 'clips_content_list')

    accordion_heads = links_div.find_elements(By.CLASS_NAME, 'zm-icon-right')
    for ahead in accordion_heads:
        ahead.click()
        time.sleep(SMALL_WAIT_TIME)

    main_div = browser.find_element(By.ID, 'recording-detail')
    meeting_name = main_div.find_element(By.CLASS_NAME, 'topic_header').text.split('\n')[0]
    info_text = main_div.find_element(By.CLASS_NAME, 'basic-info').text

    meeting_information = {
        'meeting_id': info_text.split('ID:')[1].strip(),
        'meeting_name': meeting_name,
        'meeting_info': info_text,
        'link_info': []
    }
    link_items = links_div.find_elements(By.CLASS_NAME, 'item_list')
    for link_item in link_items:
        link_text = link_item.text
        ActionChains(browser).move_to_element(link_item).perform()
        time.sleep(SMALL_WAIT_TIME)
        download_btn = link_item.find_element(By.CLASS_NAME, 'zm-icon-download-alt-thin')
        download_btn.click()
        filename = download_wait()
        meeting_information['link_info'].append({
            'link_text': link_text.split('\n')[0],
            'filename': filename,
        })
    return meeting_information

def main():
    browser = webdriver.Chrome()

    browser.get(f'{ZOOM_URL}/signin')
    time.sleep(LOGIN_TIME)
    browser.get(f'{ZOOM_URL}/recording')
    time.sleep(MED_WAIT_TIME)

    detail_links = get_detail_page_links(browser)

    link_information = []
    for dlink in detail_links:
        meeting_information = download_files(browser, dlink)
        link_information.append(meeting_information)

        with open('link_information.json', 'w') as linfo_file:
            json.dump(link_information, linfo_file, indent=2)

if __name__ == '__main__':
    main()