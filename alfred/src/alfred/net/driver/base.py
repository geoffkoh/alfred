""" Base module for alfred.net.driver """

# Standard imports
from abc import ABCMeta, abstractmethod
import logging
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
        except WebDriverException as _:
            logger.debug(traceback.format_stack())
            logger.debug('Driver for %s not detected. Skipping', key)

    return driver

# end get_web_driver()


class DriverBase(metaclass=ABCMeta):
    """ This is the base class for all the Drivers """

    # Reference to the selenium driver
    driver = None

    @abstractmethod
    def connect(self, username: str, password: str):
        raise NotImplementedError()
    # end connect()

    def navigate(self, url: str):
        """ Navigates to a particular page """
        self.driver.get(url)

# end class DriverBase()
