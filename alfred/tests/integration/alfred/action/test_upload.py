# System import
import logging
from pathlib import Path
import os

# Third party imports
import pytest

# Application import
from alfred.net.driver.myleo import MyLeoDriver
from alfred.action.upload_myleo import ActionUpload_MCQ2MyLEO
from alfred.io.question import create_from_file

logger = logging.getLogger(__name__)


@pytest.mark.skipif(
    os.getenv("ALFRED_USERNAME") is None or os.getenv("ALFRED_PASS") is None,
    reason="Username and password not given",
)
def test_upload_question_to_myleo():
    """Tests an actual uploading of question to MyLeo"""

    # Creates the driver
    driver = MyLeoDriver()
    driver.connect(
        username=os.getenv("ALFRED_USERNAME"),  # To replace with username
        password=os.getenv("ALFRED_PASS"),  # To replace with password
    )

    # Reads the questions
    sample_filename = os.path.join(
        Path(__file__).parents[3],
        "resources",
        "alfred",
        "io",
        "question",
        "sample_mcq.xlsx",
    )
    question_bank = create_from_file(sample_filename)

    # Creates the action and tries to upload the question
    action = ActionUpload_MCQ2MyLEO()
    action.run(driver=driver, bank=question_bank)


# end upload_question_to_myleo()
