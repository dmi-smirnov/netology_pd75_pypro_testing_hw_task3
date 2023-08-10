import time

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_conds

import firefox_path
import yandex_account


@pytest.fixture
def ff_path():
  return firefox_path.path

@pytest.fixture
def authorization_page_url():
  return 'https://passport.yandex.ru/auth'

@pytest.fixture
def login():
  return yandex_account.login

@pytest.fixture
def pwd():
  return yandex_account.pwd

@pytest.fixture
def personal_account_url():
  return 'https://id.yandex.ru/'

@pytest.fixture
def driver(ff_path, authorization_page_url):
  options = Options()
  options.binary = FirefoxBinary(ff_path)

  driver = webdriver.Firefox(options=options)
  yield driver
  
  # After testing
  # Logout and closing browser
  try:
    # Opening user menu
    user_menu_button = WebDriverWait(driver, 10).until(
      exp_conds.presence_of_element_located(
        (By.CSS_SELECTOR, 'button.UserID-Account')
      )
    )
    time.sleep(1)
    user_menu_button.click()

    # Switch to user menu frame
    iframe = driver.find_element(by=By.CSS_SELECTOR, value='iframe.UserWidget-Iframe')
    driver.switch_to.frame(iframe)

    # Clicking to logout button
    logout_button = WebDriverWait(driver, 10).until(
      exp_conds.presence_of_element_located(
        (By.CSS_SELECTOR, '.MenuItem_logout')
      )
    )
    time.sleep(1)
    logout_button.click()
    
    # Waiting forwarding to authorization page
    WebDriverWait(driver, 10).until(
      exp_conds.url_contains(authorization_page_url)
    )
    time.sleep(1)
  finally:
    driver.quit()

def test_auth_with_mail(driver, authorization_page_url, login, pwd,
  personal_account_url):
  # Opening authorization page
  driver.get(authorization_page_url)

  # Clicking on login type button - Mail
  driver.find_element(by=By.CSS_SELECTOR,
    value='.AuthLoginInputToggle-type button[data-type=login]').click()

  # Entering login
  driver.find_element(by=By.ID, value='passp-field-login').send_keys(login)

  # Clicking on Log in button
  driver.find_element(by=By.ID, value='passp:sign-in').click()

  # Entering password
  driver.find_element(by=By.ID, value='passp-field-passwd').send_keys(pwd)

  # Clicking on Log in button
  driver.find_element(by=By.ID, value='passp:sign-in').click()

  # Waiting forwarding to personal account page
  for _ in range(10):
    if driver.current_url == personal_account_url:
      break
    time.sleep(1)
  assert driver.current_url == personal_account_url