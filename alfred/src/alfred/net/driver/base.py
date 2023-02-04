""" Base module for alfred.net.driver """

# Standard imports
from abc import ABCMeta, abstractmethod
import logging
import json
import traceback

# Third party imports
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


def get_web_driver():
    """Helper function to detect the browser and load the driver

    Currently we only support chrome driver for Alfred as only
    chrome has the ability to log network message, which is required
    for us to be able to extract out the session key for subsequent
    communication.
    """

    supported_driver_map = {"Chrome": create_chrome_driver}

    driver = None
    for key, driver_func in supported_driver_map.items():
        try:
            logger.info("Creating driver for %s", key)
            driver = driver_func()
            return driver
        except Exception as _:
            logger.info(traceback.format_stack())
            traceback.print_stack()
            logger.info("Driver for %s not detected. Skipping", key)

    return driver


# end get_web_driver()


def create_chrome_driver():
    """Creates the chrome driver"""
    cap = DesiredCapabilities.CHROME.copy()
    cap["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
    driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=cap)
    return driver


# end create_chrome_driver()


class DriverBase(metaclass=ABCMeta):
    """This is the base class for all the Drivers"""

    # Reference to the selenium driver
    driver = None

    def __del__(self):
        """Destructor"""
        if self.driver is not None:
            logger.info("Closing driver")
            self.driver.close()

    @abstractmethod
    def connect(self, username: str, password: str):
        raise NotImplementedError()

    # end connect()

    @abstractmethod
    def is_connected(self):
        raise NotImplementedError()

    # end is_connected()

    def navigate(self, url: str):
        """Navigates to a particular page"""
        self.driver.get(url)

    def _setup_cookies(self):
        """Transfer the cookies to the request session

        We need this so that subsequent queries to the driver via API queries
        can use the necessary cookies.
        """

        # Creates the session and transfer cookies
        self.session = requests.Session()
        selenium_user_agent = self.driver.execute_script("return navigator.userAgent;")
        self.session.headers.update({"user-agent": selenium_user_agent})
        for cookie in self.driver.get_cookies():
            self.session.cookies.set(
                cookie["name"], cookie["value"], domain=cookie["domain"]
            )

    # end _setup_cookies()

    def _setup_auth_token(self):
        """Looks to extract Authorization tokens

        Chrome webdriver provides performance log to be able to parse the network
        traffic. Using this we detect the Authorization headers and keep this in the
        instance session.
        """

        logs = self.driver.get_log("performance")
        token = None
        for entry in logs:
            if "Bearer " in str(entry["message"]):
                data = json.loads(entry["message"])
                token = data["message"]["params"]["request"]["headers"]["Authorization"]
                break
        if token is not None:
            logger.info("Updating header of session")
            self.session.headers.update({"Authorization": token})

    # end _setup_auth_token()


# end class DriverBase()
