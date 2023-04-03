""" Driver for MyLEO """

# Standard imports
import logging
import time

# Third party imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Application imports
from alfred.net.driver.base import get_web_driver, DriverBase

logger = logging.getLogger(__name__)


class MyLeoDriver(DriverBase):
    """Driver class for interacting with MyLeo

    It has a internal selenium driver that serves
    as the connection to the site.
    """

    def __init__(self):
        """Constructor"""
        self.url = "https://myleo.rp.edu.sg"
        self.home_url = "https://myleo.rp.edu.sg/CoreBase/Home/Index"
        self.driver = get_web_driver()
        self.session = None

    def __del__(self):
        """Destructor"""
        if self.driver is not None:
            logger.info("Closing driver")
            self.driver.close()

    def connect(self, username: str, password: str) -> bool:
        """Connects to the MyLeo

        Args:
            username (str): The username input
            password (str): Password input

        Returns
            Boolean to indicate whether it is connected or not
        """

        if not self.is_connected():
            self.driver.get(self.url)
            
            try:
                username_elt = self.driver.find_element_by_id("userNameInput")
                password_elt = self.driver.find_element_by_id("passwordInput")
                username_elt.send_keys(username)
                password_elt.send_keys(password)
                button = self.driver.find_element_by_id("submitButton")
                button.click()
                WebDriverWait(driver=self.driver, timeout=10).until(
                    lambda x: x.execute_script("return document.readyState === 'complete'")
                )
            except NoSuchElementException as exc:
                logger.info('Log in using connect_new()')
                self.connect_new(username=username, password=password)

            if self.is_connected():
                logger.info("Login successful")
                self._setup_cookies()
                return True
            else:
                logger.warning("Cannot log in. Incorrect username or password?")
                return False

        # Creates the session and transfer cookies
        logger.info('Is connected')
        self._setup_cookies()
        return True

    # end connect()
   
    def connect_new(self, username: str, password: str) -> None:
        """ This is the updated login page

        MyLEO has updated to a new login as at 2023-04-01 so this is
        to allow the new login screen.

        Args:
            username (str): The username input
            password (str): Password input

        Returns
            None
        """

        username_elt = self.driver.find_element(By.NAME, "loginfmt")
        password_elt = self.driver.find_element(By.NAME, "passwd")
        username_elt.send_keys(username)
        password_elt.send_keys(password)

        button = self.driver.find_element_by_id("idSIButton9")
        button.click()
        time.sleep(5)  # We need to sleep a bit to allow the next screen to appear
        button = self.driver.find_element_by_id("idSIButton9")
        button.click()
        WebDriverWait(driver=self.driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

    # end connect_new()

    def is_connected(self):
        """Checks if the driver has been connected

        It does this by going to the main url. It will then
        detect the typical url when one is connected and logged
        into MyLEO.
        """

        logger.info(f'Going to {self.home_url}')
        self.driver.get(self.home_url)
        # Finds user related elements. Non logged in page should not
        # have this
        try:
            self.driver.find_element_by_id("nav-user-dropdown")
            logger.info("Is logged in")
            self._setup_cookies()
        except NoSuchElementException as exc:
            logger.info("Not logged in")
            return False
        return True

    # end is_connected()
