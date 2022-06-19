from selenium.webdriver.opera.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv


class Window:
    _window_handle: str
    _link: str

    def __init__(self, driver: WebDriver):
        load_dotenv()
        self._driver = driver
        self._wait = WebDriverWait(driver, 20)

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, "__call__"):
            def newfunc(*args, **kwargs):
                current_window = self._driver.current_window_handle
                self._driver.switch_to.window(self._window_handle)
                result = attr(*args, **kwargs)
                self._driver.switch_to.window(current_window)

                return result

            return newfunc
        else:
            return attr

    def getWindowHandle(self):
        return self._window_handle