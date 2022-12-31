# Standard imports
import logging

# Third party imports
import pytest

# Application imports
from alfred.net.driver.sa20 import SA20Driver


class TestSA20Driver:
    """ Test class for SA20Driver """

    def test_connect(self):

        driver = MyLeSA20DriveroDriver()
        driver.connect(
            username=None,  # To replace with username
            password=None  # To replace with password
        )

    # end test_connect()
