from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
import os
import pyperclip
import time

def start():
    global driver
    global wait

    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')

    # options.add_argument('--headless')

    driver = webdriver.Chrome(
        options=options
    )

    wait = WebDriverWait(driver, 30)


def auth():
    start()
    if not os.path.exists('cookies.pkl'):
        _first_auth()
    else:
        _cookies_auth()


def _first_auth():
    login = input("логин: ")
    password = input("пароль: ")
    driver.get('https://passport.yandex.ru/')
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[id="passp-field-login"]'))).send_keys(login)
    driver.find_element(By.CSS_SELECTOR, 'button[id="passp:sign-in"]').click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[id="passp-field-passwd"]'))).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[id="passp:sign-in"]').click()
    try:
        WebDriverWait(driver, 8).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="auth-challenge-descr"]')))
    except Exception as err:
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        return None

    form = driver.find_element(By.CSS_SELECTOR, 'div[class="auth-challenge-form-hint"]')
    number = form.find_element(By.TAG_NAME, 'strong').text
    driver.find_element(By.CSS_SELECTOR, 'button[data-t="button:action"]').click()
    print(f"на номер телефона {number} будет отправлен код, напишите его")
    code = input("код: ")
    field = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="CodeField-visualContent CodeField-visualContent_size_normal"]')))
    actions = ActionChains(driver)
    actions.move_to_element(field)
    actions.click()
    actions.send_keys(code)
    actions.perform()

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def _cookies_auth():
    driver.get('https://passport.yandex.ru/')
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get('https://id.yandex.ru/')


def _input_img(url):
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-tip="Вставить изображение"]'))).click()
    place = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Ссылка"]')))
    driver.execute_script("arguments[0].setAttribute('value',arguments[1])", place, url)
    place.send_keys(Keys.SPACE)
    wait.until(ec.invisibility_of_element(place))


def create_post(text, imgs):
    driver.get('https://dzen.ru/profile/editor/create')
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="author-studio-header__addButton-1Z author-studio-header__rightItemButton-3a"]'))).click()
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Создать статью"]'))).click()
    try:
        WebDriverWait(driver, 2).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="close-cross close-cross_black close-cross_size_s help-popup__close-cross"]'))).click()
    except:
        pass
    header = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="notranslate public-DraftEditor-content"]')))
    header = header.find_element(By.TAG_NAME, 'span')
    pyperclip.copy(text.split("\n")[0])
    header.send_keys(Keys.CONTROL + 'v')
    header.send_keys(Keys.CONTROL)

    document = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="zen-editor-block zen-editor-block-paragraph"]')))
    for img in imgs:
        _input_img(img)
    pyperclip.copy(text)
    document.send_keys(Keys.CONTROL + 'v')
    document.send_keys(Keys.CONTROL)

    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="Button2 Button2_view_action Button2_size_s editor-header__edit-btn"]'))).click()
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="ui-lib-button-base _is-transition-enabled ui-lib-button _size_l _view-type_carrot _width-type_regular publication-settings-actions__action"]'))).click()

    try:
        while True:
            time.sleep(1)
            captcha = WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'img[class="captcha__image"]')))
            captcha_url = captcha.get_attribute('src')
            print(captcha_url)
            code = input("введите капчу: ")
            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'input[class="ui-lib-input__control"]'))).send_keys(code)
            wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="ui-lib-button-base _is-transition-enabled ui-lib-button _size_l _view-type_carrot _width-type_regular"]'))).click()

    except:
        pass
    wait.until(ec.invisibility_of_element_located((By.CSS_SELECTOR, 'div[class="ui-lib-modal__content publication-modal"]')))


def close_driver():
    driver.close()
    driver.quit()

