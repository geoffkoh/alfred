""" Base module for alfred.net.driver """

# Standard imports
from abc import ABCMeta, abstractmethod
import logging
import requests
import traceback

# Third party imports
import chromedriver_binary
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


def get_web_driver():
    """ Helper function to detect the browser and load the driver """

    supported_driver_map = {
        'IE': webdriver.Edge,
        'Firefox': webdriver.Firefox,
        'Chrome': webdriver.Chrome,
        'Safari': webdriver.Safari
    }

    driver = None    
    for key, driver_class in supported_driver_map.items():
        try:
            logger.debug('Creating driver for %s', key)
            driver = driver_class()
            return driver
        except Exception as _:
            logger.debug(traceback.format_stack())
            logger.debug('Driver for %s not detected. Skipping', key)

    return driver

# end get_web_driver()


class DriverBase(metaclass=ABCMeta):
    """ This is the base class for all the Drivers """

    # Reference to the selenium driver
    driver = None

    def __del__(self):
        """ Destructor """
        if self.driver is not None:
            logger.info('Closing driver')
            self.driver.close()

    @abstractmethod
    def connect(self, username: str, password: str):
        raise NotImplementedError()
    # end connect()

    def navigate(self, url: str):
        """ Navigates to a particular page """
        self.driver.get(url)

    def _setup_cookies(self):
        """ Transfer the cookies to the request session """

        # Creates the session and transfer cookies
        self.session = requests.Session()
        selenium_user_agent = self.driver.execute_script("return navigator.userAgent;")
        self.session.headers.update({"user-agent": selenium_user_agent})
        for cookie in self.driver.get_cookies():
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

    # end _setup_cookies()

# end class DriverBase()
