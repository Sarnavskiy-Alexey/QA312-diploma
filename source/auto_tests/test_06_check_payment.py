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
    'Products': GL_ARGUMENTS['url'] + 'products',
    'Cart': GL_ARGUMENTS['url'] + 'view_cart',
    'Signup / Login': GL_ARGUMENTS['url'] + 'login',
    'Test Cases': GL_ARGUMENTS['url'] + 'test_cases',
    'API Testing': GL_ARGUMENTS['url'] + 'api_list',
    'Video Tutorials': 'https://www.youtube.com/c/AutomationExercise',
    'Contact us': GL_ARGUMENTS['url'] + 'contact_us',
    'Checkout': GL_ARGUMENTS['url'] + 'checkout',
    'Payment': GL_ARGUMENTS['url'] + 'payment',
    'Payment_done': GL_ARGUMENTS['url'] + 'payment_done/500'
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


def check_payment(browser_data: webdriver.Chrome | webdriver.Edge | webdriver.Firefox):
    global GL_CONST_REFERENCES, GL_ARGUMENTS

    # 1
    email = 'q@w.e'
    password = 'q'
    browser_data.get(GL_CONST_REFERENCES['Signup / Login'])
    time.sleep(1)
    login_form = browser_data.find_element(By.CLASS_NAME, 'login-form')
    email_field = login_form.find_element(By.NAME, 'email')
    email_field.click()
    email_field.send_keys(f'{email}')
    password_field = login_form.find_element(By.NAME, 'password')
    password_field.click()
    password_field.send_keys(f'{password}')
    login_button = login_form.find_element(By.CLASS_NAME, 'btn-default')
    login_button.click()
    time.sleep(1)
    
    # 2
    browser_data.get(GL_CONST_REFERENCES['Products'])
    time.sleep(1)
    features_items = browser_data.find_element(By.CLASS_NAME, 'features_items')
    first_product = features_items.find_elements(By.CLASS_NAME, 'productinfo.text-center')
    if first_product:
        first_product = first_product[0]
    else:
        logging.error(f"{browser_data.current_url} - no products in product")
    product_name = first_product.find_element(By.TAG_NAME, 'p').text
    add_to_cart_button = first_product.find_element(By.CLASS_NAME, 'btn.btn-default.add-to-cart')
    add_to_cart_button.click()
    time.sleep(1)

    # 3
    modal_content = features_items.find_element(By.CLASS_NAME, 'modal-content')
    continue_button = modal_content.find_element(By.CLASS_NAME, 'btn.btn-success.close-modal.btn-block')
    continue_button.click()
    time.sleep(1)

    # 4
    browser_data.get(GL_CONST_REFERENCES['Cart'])
    time.sleep(1)
    cart_info_table = browser_data.find_element(By.ID, 'cart_info_table')
    product_1 = cart_info_table.find_element(By.ID, 'product-1')
    cart_description = product_1.find_element(By.CLASS_NAME, 'cart_description')
    product_name_to_check = cart_description.find_element(By.TAG_NAME, 'a').text
    if product_name_to_check != product_name:
        logging.error(f"{browser_data.current_url} - added different products")
    
    # 5
    proceed_to_checkout_button = browser_data.find_element(By.CLASS_NAME, 'btn.btn-default.check_out')
    proceed_to_checkout_button.click()
    time.sleep(1)
    if browser_data.current_url != GL_CONST_REFERENCES['Checkout']:
        logging.error(f"{browser_data.current_url} - is not ./checkout url")

    # 6
    place_order = browser_data.find_element(By.CLASS_NAME, 'btn.btn-default.check_out')
    place_order.click()
    time.sleep(1)
    if browser_data.current_url != GL_CONST_REFERENCES['Payment']:
        logging.error(f"{browser_data.current_url} - is not ./payment url")
    
    # 7
    name_holder = 'Q Q'
    number_of_card = '0123456789101112'
    cvc_code = '123'
    expiration_month = '12'
    expiration_year = '2024'
    payment_form = browser_data.find_element(By.ID, 'payment-form')
    name_on_card = payment_form.find_element(By.NAME, 'name_on_card')
    name_on_card.click()
    name_on_card.send_keys(name_holder)
    card_number = payment_form.find_element(By.NAME, 'card_number')
    card_number.click()
    card_number.send_keys(number_of_card)
    cvc = payment_form.find_element(By.NAME, 'cvc')
    cvc.click()
    cvc.send_keys(cvc_code)
    expiry_month = payment_form.find_element(By.NAME, 'expiry_month')
    expiry_month.click()
    expiry_month.send_keys(expiration_month)
    expiry_year = payment_form.find_element(By.NAME, 'expiry_year')
    expiry_year.click()
    expiry_year.send_keys(expiration_year)
    submit_button = payment_form.find_element(By.ID, 'submit')
    submit_button.click()
    time.sleep(1)

    # 8
    if browser_data.current_url != GL_CONST_REFERENCES['Payment_done']:
        logging.error(f"{browser_data.current_url} - is not ./payment_done/500 url")
    
    # 9
    download_invoice = browser_data.find_element(By.CLASS_NAME, 'btn.btn-default.check_out')
    download_invoice.click()
    time.sleep(1)


def test_06_payment_chrome(browser_data_chrome, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_payment(browser_data_chrome)
    with open('source/auto_tests/tests/chrome/test_06.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_06_payment_edge(browser_data_edge, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_payment(browser_data_edge)
    with open('source/auto_tests/tests/edge/test_06.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_06_payment_firefox(browser_data_firefox, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_payment(browser_data_firefox)
    with open('source/auto_tests/tests/firefox/test_06.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)
