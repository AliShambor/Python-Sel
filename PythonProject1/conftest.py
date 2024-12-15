from time import sleep

from selenium import webdriver
import pytest
from constants import *


@pytest.fixture
def browser():
    browser = webdriver.Chrome()
    browser.get(PATH)
    yield browser
    browser.close()



