# System import
import logging
from pathlib import Path
import os

# Third party imports
import pytest

# Application import
from alfred.net.driver.myleo import MyLeoDriver
from alfred.action.upload import ActionUploadQuestion
from alfred.io.question import create_from_file

logger = logging.getLogger(__name__)


def test_upload_question_to_myleo():
    """ Tests an actual uploading of question to MyLeo """

    # Creates the driver
    driver = MyLeoDriver()
    driver.connect(
        username=None,
        password=None
    )

    # Reads the questions
    sample_filename = os.path.join(
        Path(__file__).parents[3],
        'resources', 'alfred', 'io', 'question', 'sample_mcq.xlsx'
    )
    question_bank = create_from_file(sample_filename)

    # Creates the action and tries to upload the question
    action = ActionUploadQuestion()
    action.run(driver=driver, bank=question_bank)

    # To just pause things for a while
    input()

# end upload_question_to_myleo()
