""" Driver for MyLEO """

# Standard imports
import logging

# Third party imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Application imports
from alfred.net.driver.base import (
    get_web_driver,
    DriverBase
)

logger = logging.getLogger(__name__)


class MyLeoDriver(DriverBase):
    """ Driver class for interacting with MyLeo
    
    It has a internal selenium driver that serves
    as the connection to the site.
    """

    def __init__(self):
        """ Constructor """
        self.url = 'https://myleo.rp.edu.sg'
        self.driver = get_web_driver()
        self.session = None

    def __del__(self):
        """ Destructor """
        if self.driver is not None:
            logger.info('Closing driver')
            self.driver.close()

    def connect(self, username: str, password: str):
        """ Connects to the MyLeo
        
        Args:
            username (str): The username input
            password (str): Password input
        
        Returns
            None
        """

        self.driver.get(self.url)
        username_elt = self.driver.find_element_by_id("userNameInput")
        password_elt = self.driver.find_element_by_id("passwordInput")
        username_elt.send_keys(username)
        password_elt.send_keys(password)
        button = self.driver.find_element_by_id("submitButton")
        button.click()

        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        logger.info('Login successful')

        # Creates the session and transfer cookies
        self._setup_cookies()

    # end connect()
