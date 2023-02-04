""" Driver for MySA """

# Standard imports
from dataclasses import dataclass, field
import logging
import json
from typing import Dict, List, Tuple

# Third party imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

# Application imports
from alfred.net.driver.base import get_web_driver, DriverBase

logger = logging.getLogger(__name__)


@dataclass
class AssessmentData:
    """Data structure for the minimal information for assessment"""

    # Structure that maps module, assessment, i.e. ('A3079C', 'CWF')
    # into their respective uid
    module_assessment_pairmap: Dict[Tuple[str, str], Tuple[str, str]] = field(
        default_factory=dict
    )


def parse_assessment_filter(data: Dict) -> AssessmentData:
    """Parses assessment filter

    Args:
        data (Dict): The response from asessment filter endpoint

    Returns:
        A dataclass that contains only the required info
    """

    assessment_data = AssessmentData()

    for datum in data.get("data", []):
        for entry in datum.get("assessments"):
            assessment = entry.get("assessment")
            assessment_id = entry.get("id")
            module_code = entry.get("moduleCode")
            module_id = entry.get("moduleId")
            assessment_data.module_assessment_pairmap[(module_code, assessment)] = (
                module_id,
                assessment_id,
            )

    return assessment_data


# end parse_assessment_filter()


class MySADriver(DriverBase):
    """Driver class for interacting with MySA2.0

    It has a internal selenium driver that serves
    as the connection to the site.
    """

    def __init__(self):
        """Constructor"""
        self.url = "https://mysa.rp.edu.sg"
        self.login_url = "https://mysa.rp.edu.sg/account/account/login"
        self.assessment_url = "https://mysa.rp.edu.sg/authoring/api/assessments/filter"
        self.driver = get_web_driver()
        self.session = None

    def connect(self, username: str, password: str) -> bool:
        """Connects to the MySA and authenticates

        Args:
            username (str): The username input
            password (str): Password input

        Returns
            None
        """

        if not self.is_connected():
            self.driver.get(self.login_url)
            username_elt = self.driver.find_element_by_id("userId")
            password_elt = self.driver.find_element_by_id("password")
            username_elt.send_keys(username)
            password_elt.send_keys(password)
            button = self.driver.find_element_by_id("submitForm")
            button.click()

            # Wait until the main page of SA2.0 is present, in which
            # there will be a div with id favoriteLinksContainerId
            WebDriverWait(driver=self.driver, timeout=60).until(
                EC.presence_of_element_located((By.ID, "favoriteLinksContainerId"))
            )

            try:
                self.driver.find_element_by_id("userinfo")
                logger.info("Login successful")
                self._setup_cookies()
                self._setup_auth_token()  # We need this to set Auth token
                return True
            except NoSuchElementException:
                logger.warning("Cannot log in. Incorrect username or password?")
                return False

        return True

    # end connect()

    def is_connected(self):
        """Checks if the driver has been connected

        It does this by going to the main url. It will then
        detect the typical url when one is connected and logged
        into MyLEO.
        """

        self.driver.get(self.url)
        # Finds user related elements. Non logged in page should not
        # have this
        try:
            self.driver.find_element_by_id("userinfo")
            logger.info("Is logged in")
        except NoSuchElementException as exc:
            logger.info("Not logged in")
            return False
        return True

    # end is_connected()

    def get_assessments_filter(self, offset: int = 1, limit: int = 100) -> Dict:
        """Gets the assessment filter for RP MySA 2.0

        Args:
            offset (int): Offset for searching the db. Starting from page 1
            limit (int): Number of entries per page.

        Returns:
            Response from the MySA server.
        """

        if self.session is None:
            logger.warning("The driver is not initialized yet")
            return None

        data = {
            "qualificationTypes": [],
            "moduleCodes": [],
            "cohorts": [],
            "assessments": [],
            "offset": offset,
            "limit": limit,
        }
        response = self.session.post(url=self.assessment_url, json=data, verify=False)

        if response.status_code == 200:
            body = response.content
            return_data = json.loads(body)
            return return_data
        else:
            logger.info("Unable to retrieve assessment information")
            return None

    # end get_assessments_filter()


# end class MySADriver()
