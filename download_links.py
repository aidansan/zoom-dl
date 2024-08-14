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

    with open('download_links.tsv') as infile:
        detail_links = [line.split('\t')[0] for line in infile.readlines()]
    
    detail_links = detail_links[:5]

    link_information = []
    for dlink in detail_links:
        meeting_information = download_files(browser, dlink)
        link_information.append(meeting_information)

        with open('link_information.json', 'w') as linfo_file:
            json.dump(link_information, linfo_file, indent=2)

if __name__ == '__main__':
    main()