from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

fail_symbol = ['|', '+', '=', '[', ']', ':', ';', '«', ',', '.', '/', '?', '"', "'", "\\", '*', '<', '>']

button_points = ("(//yt-icon-button[@class='dropdown-trigger style-scope ytd-menu-renderer']/button[@class='style-scope yt-icon-button'])", 'button.yt-icon-button')

def get_elements_by_css_selector(browser, css_selector):
    elements = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )
    return elements

def get_element_by_css_selector(browser, css_selector):
    element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )
    return element

def get_element_by_xpath_selector(browser, xpath_selector):
    element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_selector))
    )
    return element

youtube_link = input('Input youtube link: ')

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options)
browser.get(youtube_link)

try:
    try:
        title = browser.title
        for symbol in fail_symbol:
            title = title.replace(symbol, '')
    except:
        title = 'not found'
    print(title)
    try:
        yt_icon_button = get_element_by_css_selector(browser, button_points[1])
    except:
        yt_icon_button = get_element_by_xpath_selector(browser, button_points[0])
    time.sleep(3)
    browser.execute_script("arguments[0].click();", yt_icon_button)
    time.sleep(2)
    ytd_menu_service = get_element_by_css_selector(browser, 'ytd-menu-service-item-renderer.ytd-menu-popup-renderer')
    browser.execute_script("arguments[0].click();", ytd_menu_service)
    time.sleep(5)
    panels = browser.find_elements_by_css_selector(
                                          'ytd-transcript-body-renderer.ytd-transcript-renderer>div>div.cues>div.cue')

    founded_text = []
    for text in panels:
        if not text.text.startswith('['):
            founded_text.append(text.text)
    text = ' '.join(founded_text)
    with open(f'{title}.txt', 'w') as f:
        f.write(text)

except Exception as e:
    print('EXCEPTION ', e)
browser.close()
print('DONE')