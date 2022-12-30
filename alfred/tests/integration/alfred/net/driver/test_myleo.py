# Standard imports
import logging

# Third party imports
import pytest

# Application imports
from alfred.net.driver.myleo import MyLeoDriver


class TestMyLeoDriver:
    """ Test class for MyLeoDriver """

    def test_connect(self):

        driver = MyLeoDriver()
        driver.connect(
            username=None,  # To replace with username
            password=None  # To replace with password
        )

    # end test_connect()
