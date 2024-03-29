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
 
    # Case 2: Reads version where the headers are one row
    sample_filename = os.path.join(
        Path(__file__).parents[3],
        "resources",
        "alfred",
        "io",
        "question",
        "sample_mcq_1.0.3.xlsx",
    )
    question_bank = create_from_file(sample_filename)
    assert question_bank is not None
    assert len(question_bank.questions) == 3, "There should be only 3 questions"
    # Assert that all the scores are either 1 or 0
    assert question_bank.questions[0].a_score in (1, 0)
    assert question_bank.questions[0].c_score in (1, 0)
    assert question_bank.questions[0].p_score in (1, 0)
    assert question_bank.questions[1].a_score in (1, 0)
    assert question_bank.questions[1].c_score in (1, 0)
    assert question_bank.questions[1].p_score in (1, 0)
    assert question_bank.questions[2].a_score in (1, 0)
    assert question_bank.questions[2].c_score in (1, 0)
    assert question_bank.questions[2].p_score in (1, 0)

# end test_create_from_file()
