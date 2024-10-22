# ##########################################################
#              (c) by Sarnavskiy, 2024, TOP
# ##########################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import chrome, edge, firefox
import pytest
import logging
import time
import random


GL_ARGUMENTS = {
    'size': '--window-size=1250,500',
    'extensions': '--disable-extensions',
    'url': 'https://www.automationexercise.com/'
}

GL_CONST_REFERENCES = {
    'Signup / Login': GL_ARGUMENTS['url'] + 'login',
    'Logout': GL_ARGUMENTS['url'] + 'logout',
    'Delete Account': GL_ARGUMENTS['url'] + 'delete_account',
    'Logged in as ': '',
    'Account Created': GL_ARGUMENTS['url'] + 'account_created'
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


def check_registration(browser_data: webdriver.Chrome | webdriver.Edge | webdriver.Firefox):
    global GL_CONST_REFERENCES
    
    # 1
    browser_data.get(GL_CONST_REFERENCES['Signup / Login'])

    # 2
    random_number = random.randint(1, 10000)
    name = f'User'
    login = f'user_{str(random_number)}@gmail.com'
    signup_form = browser_data.find_element(By.CLASS_NAME, 'signup-form')
    name_field = signup_form.find_element(By.NAME, 'name')
    name_field.click()
    name_field.send_keys(f'{name}')
    email_field = signup_form.find_element(By.NAME, 'email')
    email_field.click()
    email_field.send_keys(f'{login}')
    signup_button = signup_form.find_element(By.CLASS_NAME, 'btn-default')
    time.sleep(1)
    signup_button.click()

    # 3
    login_form = browser_data.find_element(By.CLASS_NAME, 'login-form')
    title_radio = login_form.find_element(By.CLASS_NAME, 'clearfix')
    title = title_radio.find_element(By.CSS_SELECTOR, '#id_gender1' if random_number % 2 == 0 else '#id_gender2')
    title.click()
    password = f'user_{random_number}'
    password_field = login_form.find_element(By.CSS_SELECTOR, '#password')
    password_field.click()
    password_field.send_keys(f'{password}')
    first_name_field = login_form.find_element(By.CSS_SELECTOR, '#first_name')
    first_name_field.click()
    first_name_field.send_keys('New')
    last_name_field = login_form.find_element(By.CSS_SELECTOR, '#last_name')
    last_name_field.click()
    last_name_field.send_keys('User')
    address_field = login_form.find_element(By.CSS_SELECTOR, '#address1')
    address_field.click()
    address_field.send_keys(f'Some new user {random_number} address')
    country_field = login_form.find_element(By.CSS_SELECTOR, '#country')
    country_field = country_field.find_element(By.XPATH, '//*[@id="country"]/option[2]')
    country_field.click()
    state_field = login_form.find_element(By.CSS_SELECTOR, '#state')
    state_field.click()
    state_field.send_keys(f'New-State')
    city_field = login_form.find_element(By.CSS_SELECTOR, '#city')
    city_field.click()
    city_field.send_keys(f'New-City')
    zipcode_field = login_form.find_element(By.CSS_SELECTOR, '#zipcode')
    zipcode_field.click()
    zipcode_field.send_keys(f'12345')
    mobile_number_field = login_form.find_element(By.CSS_SELECTOR, '#mobile_number')
    mobile_number_field.click()
    mobile_number_field.send_keys(f'+79012345678')
    create_account_button = browser_data.find_element(By.XPATH, '//*[@id="form"]/div/div/div/div/form/button')
    time.sleep(1)
    create_account_button.click()

    # 4
    time.sleep(5)
    error = False
    if browser_data.current_url != GL_CONST_REFERENCES['Account Created']:
        logging.error(f"{browser_data.current_url} - switching on {GL_CONST_REFERENCES['Account Created']} is not successful")
        error = True
    elif 'Automation Exercise' not in browser_data.title:
        logging.error(f"{browser_data.current_url} - 'Automation Exercise' is not found!")
        error = True
    elif 'Account Created' not in browser_data.title:
        logging.error(f"{browser_data.current_url} - 'Account Created' is not found!")
        error = True

    # 5
    navigation_menu = browser_data.find_element(By.CLASS_NAME, 'navbar-nav')
    navigation_menu = navigation_menu.find_elements(By.TAG_NAME, 'li')
    logout_error, delete_account_error, logged_in_as_error = True, True, True
    
    for btn in navigation_menu:
        reference = btn.find_element(By.TAG_NAME, 'a')
        btn_name = btn.text.replace('\ue8f8', '').lstrip()
        if btn_name == 'Logout' and reference.get_attribute('href') == GL_CONST_REFERENCES[btn_name]:
            logout_error = False
        if btn_name == 'Delete Account' and reference.get_attribute('href') == GL_CONST_REFERENCES[btn_name]:
            delete_account_error = False
        if btn_name == 'Logged in as ' + name:
            logged_in_as_error = False
    
    if logout_error:
        logging.error('\"Logout\" button is absent')
    if delete_account_error:
        logging.error('\"Delete Account\" button is absent')
    if logged_in_as_error:
        logging.error(f'\"Logged in as {name}\" button is absent')
    
    # 6
    continue_button = browser_data.find_element(By.XPATH, '//*[@id="form"]/div/div/div/div/a')
    continue_button.click()

    # 7
    time.sleep(2)
    browser_data.get(GL_CONST_REFERENCES['Delete Account'])
    time.sleep(2)
    error = False
    if browser_data.current_url != GL_CONST_REFERENCES['Delete Account']:
        logging.error(f"{browser_data.current_url} - switching on {GL_CONST_REFERENCES['Delete Account']} is not successful")
        error = True
    elif 'Automation Exercise' not in browser_data.title:
        logging.error(f"{browser_data.current_url} - 'Automation Exercise' is not found!")
        error = True
    elif 'Account Deleted' not in browser_data.title:
        logging.error(f"{browser_data.current_url} - 'Account Deleted' is not found!")
        error = True
    
    # 8
    time.sleep(2)
    browser_data.get(GL_CONST_REFERENCES['Signup / Login'])
    login_form = browser_data.find_element(By.CLASS_NAME, 'login-form')
    email_field = login_form.find_element(By.NAME, 'email')
    email_field.click()
    email_field.send_keys(f'{login}')
    password_field = login_form.find_element(By.NAME, 'password')
    password_field.click()
    password_field.send_keys(f'{name}')
    login_button = login_form.find_element(By.CLASS_NAME, 'btn-default')
    time.sleep(1)
    login_button.click()

    # 9
    time.sleep(1)
    warning_paragraph = browser_data.find_element(By.XPATH, '//*[@id="form"]/div/div/div[1]/div/form/p')
    if not warning_paragraph.is_displayed() or warning_paragraph.text != 'Your email or password is incorrect!':
        logging.error(f"{browser_data.current_url} - 'Your email or password is incorrect!' paragraph is not found!")


def test_03_registration_chrome(browser_data_chrome, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_registration(browser_data_chrome)
    with open('source/auto_tests/tests/chrome/test_03.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_03_registration_edge(browser_data_edge, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_registration(browser_data_edge)
    with open('source/auto_tests/tests/edge/test_03.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_03_registration_firefox(browser_data_firefox, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_registration(browser_data_firefox)
    with open('source/auto_tests/tests/firefox/test_03.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)
