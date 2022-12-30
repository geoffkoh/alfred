# Standard imports
import logging

# Third party imports
import pytest

# Application imports
from alfred.net.driver.base import get_web_driver


def test_get_web_driver():
    """ Tests the get_web_driver function """

    driver = get_web_driver()
    assert driver is not None

# end test_get_web_driver()
