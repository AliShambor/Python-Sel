from time import sleep

from constants import PATH
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def login(browser):
    with open('users.json', 'r') as file:
        data = json.load(file)

    browser.find_element(By.XPATH, "//button[@data-test-id='qa-header-login-button']").click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "qa-login-email-input")))
    email_element = browser.find_element(By.ID, "qa-login-email-input")
    email_element.send_keys(data[0]['username'])
    pass_element = browser.find_element(By.ID, "qa-login-password-input")
    pass_element.send_keys(data[0]['password'])
    browser.find_element(By.XPATH, "//button[@data-test-id='qa-login-submit']").click()
    sleep(3)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='qa-header-profile-button']")))

def search(browser, str_to_search):
    search_element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='qa-header-search-button']")))
    search_element.click()
    search_box = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@data-test-id='qa-search-box-input']")))
    search_box.send_keys(str_to_search)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Hello kitty')]")))


def test_terminal_x(browser):
    res = True
    error_list = []
    login(browser)
    search(browser, 'hello')

    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='list_3tWy']")))
    lists =  browser.find_elements(By.XPATH, "//ul[@class='list_3tWy']") #
    items = lists[1].find_elements(By.TAG_NAME, 'li')
    texts = []
    for item in items:
        texts.append(float(item.find_element(By.XPATH, ".//div[@class='row_2tcG bold_2wBM']").text.split()[0]))

    if texts != sorted(texts):
        res = False
        error_list.append(f'products are no sorted by price\n'
                          f'{texts}')
    items[2].find_element(By.TAG_NAME, 'a').click()
    price = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='qa-pdp-price-final']")))
    font_size = price.value_of_css_property('font-size')
    if font_size != '19.44px':  # the font size appear on px not rem on my browser
        res = False
        error_list.append('wrong font size')

    if not res:
        raise Exception(f"Test Failed\n {error_list}")
