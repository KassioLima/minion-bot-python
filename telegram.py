import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.opera.webdriver import WebDriver
from window import Window
from os import getenv


class Telegram(Window):

    def __init__(self, driver: WebDriver, blazeWindowHandle: str):
        super().__init__(driver)
        self._telegramLink = getenv("TELEGRAM_LINK")
        self._telegramPhoneNumber = getenv("TELEGRAM_PHONE_NUMBER")

        self._driver.execute_script("window.open();")
        self._wait.until(EC.number_of_windows_to_be(2))

        for window_handle in self._driver.window_handles:
            if window_handle != blazeWindowHandle:
                self._window_handle = window_handle
                self._driver.switch_to.window(self._window_handle)
                break

        self._driver.get(self._telegramLink)
        self._wait.until(EC.title_contains("Telegram"))
        self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary.btn-secondary.btn-primary-transparent.primary.rp")))
        time.sleep(5)
        self._driver.find_element(By.CLASS_NAME, "btn-primary.btn-secondary.btn-primary-transparent.primary.rp").click()
        time.sleep(5)
        self._driver.execute_script("arguments[0].innerText = '" + self._telegramPhoneNumber + "'", self._driver.find_elements(By.CLASS_NAME, "input-field-input")[1])
        self._driver.find_element(By.CLASS_NAME, "btn-primary.btn-color-primary.rp").click()

    def getAllMessageElements(self):
        time.sleep(1)
        return self._driver.find_elements(By.CLASS_NAME, "message")