# Standard imports
import logging
from pathlib import Path
import os

# Third party imports
import pytest

# Application imports
from alfred.action.upload_myleo import ActionUpload_MCQ2MyLEO
from alfred.io.question import create_from_file
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

    @pytest.mark.skip(reason="To run only if we want to test question upload")
    def test_upload_question(self):
        """ Tests upload of question """

        sample_filename = os.path.join(
            Path(__file__).parents[4],
            "resources",
            "alfred",
            "io",
            "question",
            "sample_mcq_1.0.3.xlsx",
        )
        question_bank = create_from_file(sample_filename)

        driver = MyLeoDriver()
        driver.connect(
            username=os.getenv("ALFRED_USERNAME"),  # To replace with username
            password=os.getenv("ALFRED_PASS"),  # To replace with password
        )

        action = ActionUpload_MCQ2MyLEO()
        action.run(driver=driver, bank=question_bank)

    # end test_upload_question()
