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
    'Products': GL_ARGUMENTS['url'] + 'products',
    'Cart': GL_ARGUMENTS['url'] + 'view_cart',
    'Signup / Login': GL_ARGUMENTS['url'] + 'login',
    'Test Cases': GL_ARGUMENTS['url'] + 'test_cases',
    'API Testing': GL_ARGUMENTS['url'] + 'api_list',
    'Video Tutorials': 'https://www.youtube.com/c/AutomationExercise',
    'Contact us': GL_ARGUMENTS['url'] + 'contact_us'
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


def check_navigation_menu(browser_data: webdriver.Chrome | webdriver.Edge | webdriver.Firefox):
    global GL_CONST_REFERENCES, GL_ARGUMENTS

    for key in GL_CONST_REFERENCES:
        if not GL_ARGUMENTS['url'] in GL_CONST_REFERENCES[key]:
            continue
        
        browser_data.get(GL_CONST_REFERENCES[key])
        if 'Automation Exercise' not in browser_data.title:
            logging.error(f"{browser_data.current_url} - 'Automation Exercise' is not found!")
        else:
            navigation_menu = browser_data.find_element(By.CLASS_NAME, 'navbar-nav')
            navigation_menu = navigation_menu.find_elements(By.TAG_NAME, 'li')
            for btn in navigation_menu:
                reference = btn.find_element(By.TAG_NAME, 'a')
                btn_name = btn.text.replace('\ue8f8', '').lstrip()
                
                if btn_name not in GL_CONST_REFERENCES.keys():
                    logging.error(f"{btn_name} does not equal for declared name!")
                elif reference.get_attribute('href') != GL_CONST_REFERENCES[btn_name]:
                    logging.error(f"{reference.get_attribute('href')} is not equal for {GL_CONST_REFERENCES[btn_name]}")


def test_01_navigation_menu_chrome(browser_data_chrome, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_navigation_menu(browser_data_chrome)
    with open('source/auto_tests/tests/chrome/test_01.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_01_navigation_menu_edge(browser_data_edge, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_navigation_menu(browser_data_edge)
    with open('source/auto_tests/tests/edge/test_01.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_01_navigation_menu_firefox(browser_data_firefox, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_navigation_menu(browser_data_firefox)
    with open('source/auto_tests/tests/firefox/test_01.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)
