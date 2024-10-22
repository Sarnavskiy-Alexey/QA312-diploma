# ##########################################################
#              (c) by Sarnavskiy, 2024, TOP
# ##########################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import chrome, edge, firefox
import pytest
import logging
import time


GL_ARGUMENTS = {
    'size': '--window-size=1250,500',
    'extensions': '--disable-extensions',
    'url': 'https://www.automationexercise.com/'
}

GL_CONST_REFERENCES = {
    'Home': GL_ARGUMENTS['url'] + '',
    'Products': GL_ARGUMENTS['url'] + 'products'
}


def get_browser(class_browser: webdriver.Chrome | webdriver.Edge | webdriver.Firefox, option_func):
    global GL_ARGUMENTS
    options = option_func()
    options.add_argument(GL_ARGUMENTS['extensions'])
    browser = class_browser(options=options)
    browser.maximize_window()
    # browser.get(GL_ARGUMENTS['url'])
    implicitly_wait_time = 2
    browser.implicitly_wait(implicitly_wait_time)
    
    return browser


@pytest.fixture()
def browser_data_chrome():
    browser = get_browser(webdriver.Chrome, chrome.options.Options)
    yield browser
    browser.close()


@pytest.fixture()
def browser_data_edge():
    browser = get_browser(webdriver.Edge, edge.options.Options)
    yield browser
    browser.close()


@pytest.fixture()
def browser_data_firefox():
    browser = get_browser(webdriver.Firefox, firefox.options.Options)
    yield browser
    browser.close()


def check_brand_menu(browser_data: webdriver.Chrome | webdriver.Edge | webdriver.Firefox):
    global GL_CONST_REFERENCES, GL_ARGUMENTS

    for key in GL_CONST_REFERENCES:
        browser_data.get(GL_CONST_REFERENCES[key])
        brand_menu = browser_data.find_element(By.CLASS_NAME, 'brands_products')
        brand_menu = brand_menu.find_elements(By.TAG_NAME, 'li')
        for btn in brand_menu:
            reference = btn.find_element(By.TAG_NAME, 'a')
            btn_name = reference.text
            checkable_reference = GL_ARGUMENTS['url'] + 'brand_products/' + btn_name

            if reference.get_attribute('href') != checkable_reference:
                logging.error(f"{checkable_reference} is not equal for {reference}!")


def test_02_brand_menu_chrome(browser_data_chrome, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_brand_menu(browser_data_chrome)
    with open('source/auto_tests/tests/chrome/test_02.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_02_brand_menu_edge(browser_data_edge, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_brand_menu(browser_data_edge)
    with open('source/auto_tests/tests/edge/test_02.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_02_brand_menu_firefox(browser_data_firefox, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_brand_menu(browser_data_firefox)
    with open('source/auto_tests/tests/firefox/test_02.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)
