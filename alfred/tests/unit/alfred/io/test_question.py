# Standard imports
import logging
import os
from pathlib import Path

# Third party imports
import pytest

# Application imports
from alfred.io.question import create_from_file


def test_create_from_file():
    """Tests creating a databank from file"""

    # Gets the sample filename
    sample_filename = os.path.join(
        Path(__file__).parents[3],
        "resources",
        "alfred",
        "io",
        "question",
        "sample_mcq_1.0.1.xlsx",
    )

    question_bank = create_from_file(sample_filename)
    assert question_bank is not None
    assert len(question_bank.questions) == 3, "There should be only 3 questions"
    assert question_bank.questions[0].content.startswith("Calculate the molar mass")
    assert len(question_bank.questions[0].options) == 4
    for question in question_bank.questions:
        assert question.module == "A3079C"
        assert question.assessment == "CWF"

    # Tries reading in new version
    sample_filename = os.path.join(
        Path(__file__).parents[3],
        "resources",
        "alfred",
        "io",
        "question",
        "sample_mcq_1.0.2.xlsx",
    )

    question_bank = create_from_file(sample_filename)
    assert question_bank is not None
    assert len(question_bank.questions) == 3, "There should be only 3 questions"
    assert question_bank.questions[0].content.startswith("Calculate the molar mass")
    assert len(question_bank.questions[0].options) == 4
    for question in question_bank.questions:
        assert question.module == "A3079C"
        assert question.assessment == "CW1"
        assert question.qtype == "CET (AY2022 Term 4)"
 
# end test_create_from_file()
