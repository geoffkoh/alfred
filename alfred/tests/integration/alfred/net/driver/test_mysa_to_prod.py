# Standard imports
import logging
import os

# Third party imports
import pytest

# Application imports
from alfred.net.driver.mysa import MySADriver, parse_assessment_filter

logger = logging.getLogger(__name__)


class TestMySADriver:
    """Test class for SA20Driver"""

    @pytest.mark.skipif(
        os.getenv("ALFRED_USERNAME") is None or os.getenv("ALFRED_PASS") is None,
        reason="Username and password not given",
    )
    def test_connect(self):

        driver = MySADriver()
        result = driver.connect(
            username=os.getenv("ALFRED_USERNAME"),  # To replace with username
            password=os.getenv("ALFRED_PASS"),  # To replace with password
        )

        assert result, "Should be logged in successfully"

    # end test_connect()

    @pytest.mark.skipif(
        os.getenv("ALFRED_USERNAME") is None or os.getenv("ALFRED_PASS") is None,
        reason="Username and password not given",
    )
    def test_get_assessments_filter(self):
        """Tests uploading of a sample file"""

        driver = MySADriver()
        driver.connect(
            username=os.getenv("ALFRED_USERNAME"),  # To replace with username
            password=os.getenv("ALFRED_PASS"),  # To replace with password
        )

        assessment = driver.get_assessments_filter()
        parsed_data = parse_assessment_filter(assessment)
        assert parsed_data is not None

    # end test_get_assessments_filter()


# end TestMySADriver()
