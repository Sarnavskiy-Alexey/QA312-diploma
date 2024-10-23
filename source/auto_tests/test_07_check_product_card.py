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


def check_product_card(browser_data: webdriver.Chrome | webdriver.Edge | webdriver.Firefox):
    global GL_CONST_REFERENCES, GL_ARGUMENTS

    # 1
    browser_data.get(GL_CONST_REFERENCES['Products'])
    time.sleep(1)
    features_items = browser_data.find_element(By.CLASS_NAME, 'features_items')
    first_product = features_items.find_elements(By.CLASS_NAME, 'productinfo.text-center')
    if first_product:
        first_product = first_product[0]
    else:
        logging.error(f"{browser_data.current_url} - no products in product")
    product_name = first_product.find_element(By.TAG_NAME, 'p').text
    col_sm_4 = features_items.find_elements(By.CLASS_NAME, 'col-sm-4')[0]
    choose_div = col_sm_4.find_element(By.CLASS_NAME, 'choose')
    view_product_button = choose_div.find_element(By.TAG_NAME, 'a')
    view_product_button.click()
    time.sleep(1)

    # 2
    review_form = browser_data.find_element(By.ID, 'review-form')
    name = review_form.find_element(By.ID, 'name')
    name.click()
    name.send_keys('Q')
    email = review_form.find_element(By.ID, 'email')
    email.click()
    email.send_keys('q@w.e')
    review = review_form.find_element(By.ID, 'review')
    review.click()
    review.send_keys('My review')
    review_button = review_form.find_element(By.ID, 'button-review')
    review_button.click()
    time.sleep(0.2)
    review_section = browser_data.find_element(By.ID, 'review-section')
    review_thanks = review_section.find_element(By.TAG_NAME, 'span')
    if review_thanks != 'Thank you for your review.':
        logging.error(f"{browser_data.current_url} - thanks for review were not given")
    time.sleep(1)
    
    # 3
    product_information = browser_data.find_element(By.CLASS_NAME, 'product-information')
    number_input = product_information.find_element(By.ID, 'quantity')
    number_input.click()
    number_input.clear()
    number_input.send_keys('5')
    time.sleep(0.5)

    # 4
    number_input.send_keys(Keys.ARROW_UP)
    time.sleep(0.5)
    if number_input.text != '6':
        logging.error(f"{browser_data.current_url} - up arrow does not work")

    # 5
    number_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    number_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    if number_input.text != '4':
        logging.error(f"{browser_data.current_url} - down arrow does not work")
    
    # 6
    add_to_cart_button = product_information.find_element(By.CLASS_NAME, 'btn.btn-default.cart')
    add_to_cart_button.click()
    time.sleep(1)
    
    # 7
    browser_data.get(GL_CONST_REFERENCES['Cart'])
    time.sleep(1)
    cart_info_table = browser_data.find_element(By.ID, 'cart_info_table')
    product_1 = cart_info_table.find_element(By.ID, 'product-1')
    cart_description = product_1.find_element(By.CLASS_NAME, 'cart_description')
    product_name_to_check = cart_description.find_element(By.TAG_NAME, 'a').text
    if product_name_to_check != product_name:
        logging.error(f"{browser_data.current_url} - added different products")
    cart_quantity = product_1.find_element(By.CLASS_NAME, 'cart_quantity').text
    if cart_quantity != '4':
        logging.error(f"{browser_data.current_url} - product quantity is not the same as expected")


def test_07_prodduct_card_chrome(browser_data_chrome, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_product_card(browser_data_chrome)
    with open('source/auto_tests/tests/chrome/test_07.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_07_prodduct_card_edge(browser_data_edge, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_product_card(browser_data_edge)
    with open('source/auto_tests/tests/edge/test_07.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)


def test_07_prodduct_card_firefox(browser_data_firefox, caplog):
    time.sleep(2)
    caplog.set_level(logging.INFO)
    check_product_card(browser_data_firefox)
    with open('source/auto_tests/tests/firefox/test_07.log', mode='wt') as f:
        for line in caplog.text:
            f.write(line)
