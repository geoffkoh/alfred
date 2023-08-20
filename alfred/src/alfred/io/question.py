# Standard imports
from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import List

# Third party imports
import pandas as pd
import numpy as np
import openpyxl

# Application imports

logger = logging.getLogger(__name__)


@dataclass
class Question:
    """Class representing a single question"""

    title: str = field(default=None)
    score: float = field(default=0)
    est_time_min: int = field(default=0)


@dataclass
class CompetencyMixin:
    """Mixin dataclass to denote that there is competency score"""

    c_score: int = field(default=0)
    p_score: int = field(default=0)
    a_score: int = field(default=0)


@dataclass
class MultipleChoiceQuestion(Question, CompetencyMixin):
    """Class representing a multiple choice question"""

    content: str = field(default=None)
    answer: str = field(default=None)
    options: dict = field(default_factory=dict)
    module: str = None  # The module code, e.g. A3079C
    assessment: str = None  # Assessment e.g. CW1
    qtype: str = None  # Qualification type, e.g. PFP (AY2022 Semester 2)


@dataclass
class QuestionBank:
    """Structure to hold the questions"""

    questions: List[Question] = field(default_factory=list)


class ParseState(Enum):
    NOT_QUESTION = "NOT_QUESTION"
    QUESTION = "QUESTION"
    CHOICE = "CHOICE"


def create_from_file(filename: str) -> QuestionBank:
    """Creates a question bank from file

    Args:
        filename (str): The filename of the excel spreadsheet

    Returns:
        A parsed question bank containing all the questions.
    """

    # Opens up the file
    # We assume that the question is in the first
    # spread sheet and we read everything
    # into a dataframe first
    data = pd.read_excel(filename)

    # Update column names if just A, P, C are found
    # as they should be 'A marks', 'P marks', 'C marks'
    if 'A' in data.columns and 'A marks' not in data.columns:
        data.rename(columns={"A": "A marks"}, inplace=True)
    if 'P' in data.columns and 'P marks' not in data.columns:
        data.rename(columns={"P": "P marks"}, inplace=True)
    if 'C' in data.columns and 'C marks' not in data.columns:
        data.rename(columns={"C": "C marks"}, inplace=True)

    logger.info("Creating new question bank")
    question_bank = QuestionBank()
    question = None

    curr_state = ParseState.NOT_QUESTION
    curr_module = None
    curr_assessment = None
    curr_qtype = None
    for index, row in data.iterrows():

        # Determines the current state.
        if pd.notnull(row.Question):
            if pd.notnull(row.Score):
                curr_state = ParseState.QUESTION
            else:
                curr_state = ParseState.CHOICE
        else:
            curr_state = ParseState.NOT_QUESTION

        logger.debug("Current state %s", curr_state)
        # Parses the line depending on the curr state
        if curr_state == ParseState.QUESTION:
            question = MultipleChoiceQuestion()
            question_bank.questions.append(question)
            question.title = row.Title
            question.content = row.Question
            question.score = row.Score
            question.answer = row.Ans
            question.est_time_min = row["Est.time (min)"]
            question.a_score = float(row["A marks"]) if not pd.isna(row["A marks"]) else 0
            question.c_score = float(row["C marks"]) if not pd.isna(row["C marks"]) else 0
            question.p_score = float(row["P marks"]) if not pd.isna(row["P marks"]) else 0

            if "Module Code" in data:
                if row["Module Code"] is not np.nan:
                    question.module = row["Module Code"]
                    curr_module = question.module
                else:
                    question.module = curr_module
            if "Assessment Type" in data:
                if row["Assessment Type"] is not np.nan:
                    question.assessment = row["Assessment Type"]
                    curr_assessment = question.assessment
                else:
                    question.assessment = curr_assessment
            if "Qualification Type" in data:
                if row["Qualification Type"] is not np.nan:
                    question.qtype = row["Qualification Type"]
                    curr_qtype = question.qtype
                else:
                    question.qtype = curr_qtype
        elif curr_state == ParseState.CHOICE:
            question.options[row.Title] = str(row.Question)
        else:
            question = None

    return question_bank


# end create_from_file()
