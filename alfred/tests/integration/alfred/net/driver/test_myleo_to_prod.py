# Standard imports
import logging
import os

# Third party imports
import pytest

# Application imports
from alfred.net.driver.myleo import MyLeoDriver


class TestMyLeoDriver:
    """Test class for MyLeoDriver"""

    @pytest.mark.skipif(
        os.getenv("ALFRED_USERNAME") is None or os.getenv("ALFRED_PASS") is None,
        reason="Username and password not given",
    )
    def test_connect(self):

        driver = MyLeoDriver()
        driver.connect(
            username=os.getenv("ALFRED_USERNAME"),  # To replace with username
            password=os.getenv("ALFRED_PASS"),  # To replace with password
        )

    # end test_connect()
