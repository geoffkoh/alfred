""" Driver for SA2.0 """

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


class SA20Driver(DriverBase):
    """ Driver class for interacting with SA2.0
    
    It has a internal selenium driver that serves
    as the connection to the site.
    """

    def __init__(self):
        """ Constructor """
        self.url = 'https://mysa.rp.edu.sg/account/account/login'
        self.driver = get_web_driver()
        self.session = None

    def connect(self, username: str, password: str):
        """ Connects to the MyLeo
        
        Args:
            username (str): The username input
            password (str): Password input
        
        Returns
            None
        """

        self.driver.get(self.url)

        username_elt = self.driver.find_element_by_id("userId")
        password_elt = self.driver.find_element_by_id("password")
        username_elt.send_keys(username)
        password_elt.send_keys(password)
        button = self.driver.find_element_by_id("submitForm")
        button.click()

        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        logger.info('Login successful')

        # Creates the session and transfer cookies
        self._setup_cookies()

    # end connect()
