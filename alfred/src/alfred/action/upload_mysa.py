""" Action for uploading questions to RP MySA 2.0 """

# Standard import
from dataclasses import asdict, dataclass, field
from html import escape
import json
import logging
import pprint
import traceback
from typing import Dict, List

# Application import
from alfred.net.driver.base import DriverBase
from alfred.net.driver.mysa import parse_assessment_filter
from alfred.io.question import QuestionBank, MultipleChoiceQuestion

logger = logging.getLogger(__name__)


@dataclass
class Payload:
    """This is the payload to send to the API for creating a question to MySA 2.0"""

    type: int = 0
    title: str = None  # Require user input
    comment: str = ""
    topicList: List[str] = None
    topics: List[str] = field(default_factory=list)
    learningOutcomes: str = ""
    estimatedTime: int = 1
    proficiencyLevel: str = None
    hasDependency: bool = False
    dependencies: List[str] = field(default_factory=list)
    useTos: bool = False
    score: int = 1  # Require user input
    materials: List[str] = field(default_factory=list)
    displayObj: str = None
    assessmentId: str = None  # Require user input
    moduleCode: str = None  # Require user input
    tosItemId: str = None
    bankType: int = 0
    questionGroups: List[str] = field(default_factory=list)
    content: str = None  # Require user input
    markingScheme: str = None  # Require user input
    status: int = 1


# end class Payload


@dataclass
class PayloadContent:
    """Content portion of the payload"""

    allowRandom: bool = True
    # This is for competency scores, i.e. {'displayName': 'Competent', 'score': 1}
    difficultyScores: List = field(default_factory=list)
    displayStructure: int = 1
    # For the individual options
    # {'content': str, 'id': 'choice_0/1/2/3'}
    options: List = field(default_factory=list)
    question: str = None


def render_question(question: str) -> str:
    """Renders the question to be input"""
    content = (
        "<span "
        'data-default-style="{&quot;fontFamily&quot;:&quot;Arial&quot;,&quot;fontSize&quot;:&quot;12pt&quot;}" '
        f'style="font-family: Arial; font-size: 12pt;">{escape(question)}</span>'
    )
    return content


def render_options(option: str) -> str:
    """Renders the option for input"""
    content = (
        "<span "
        'data-default-style="{&quot;fontFamily&quot;:&quot;Arial&quot;,&quot;fontSize&quot;:&quot;12pt&quot;}" '
        f'style="font-family: Arial; font-size:12pt;">{escape(option)}</span>'
    )
    return content


@dataclass
class PayloadMarkingScheme:
    """The Marking scheme of the Payload"""

    scoreType: int = 0
    # The list of correct answers
    # {"id": "choice_3"}
    correctAnswers: List = field(default_factory=list)
    markingSchemeText: str = ""


# end class PayloadMarkingScheme


class ActionUpload_MCQ2MySA:
    """Action to upload MCQ Question to RP MySA 2.0"""

    def __init__(self):
        """Constructor"""
        self.url = "https://mysa.rp.edu.sg/authoring"
        self.create_api = "https://mysa.rp.edu.sg/authoring/api/questions"
        self.assessment_filter = None

    # end __init__()

    def run(self, driver: DriverBase, bank: QuestionBank) -> bool:
        """Runs this particular action"""

        logger.info("Getting assessment filter")
        self.assessment = parse_assessment_filter(driver.get_assessments_filter())
        logger.info("Received assessment filter")
        logger.info("%s", pprint.pformat(self.assessment.module_assessment_map))

        logger.info("Creating questions")
        counter = 0
        for question in bank.questions:
            try:
                if self.create_question(driver=driver, question=question):
                    counter += 1
            except ValueError as exc:
                logger.error(traceback.format_exc())
                logger.error(exc)
        logger.info("%s/%s Questions created", counter, len(bank.questions))

        driver.navigate(self.url)
        return True

    # end run()

    def create_question(
        self, driver: DriverBase, question: MultipleChoiceQuestion
    ) -> bool:
        """Creates a multiple choice question

        Args:
            driver (DriverBase): The driver for the connection to MySA
            question (MultipleChoiceQuestion): Instance of multiple choice questions.

        """

        logger.info("Creating question: %s", question.title)

        payload = Payload()
        payload.title = question.title
        payload.score = int(question.score)
        payload.estimatedTime = int(question.est_time_min)

        # If the qtype is empty, and there is only one module-assessment
        # entry, then we still add it in.
        mod_assess_entries = self.assessment.module_assessment_map.get(
            (question.module, question.assessment)
        )
        if not question.qtype:
            if len(mod_assess_entries) == 0:
                logger.error(
                    'Module %s Assessment %s with correct rights cannot be found. '
                    'Skipping question: %s',
                    question.module, question.assessment, question.title
                )
                return False
            elif len(mod_assess_entries) > 1:
                logger.error(
                    'Module %s Assessment %s has more than 1 entry. '
                    'Please provide qualification type in question. '
                    'Skipping question: %s',
                    question.module, question.assessment, question.title
                )
                return False
            else:
                mod_assess_pair = list(mod_assess_entries.values())[0]
        else:
            if question.qtype not in mod_assess_entries:
                logger.error(
                    'Module %s Assessment %s QType %s not found. '
                    'Skipping question: %s',
                    question.module, question.assessment, question.qtype, question.title
                )
                return False
            else:
                mod_assess_pair = mod_assess_entries.get(question.qtype)

        payload.assessmentId = mod_assess_pair[1]
        payload.moduleCode = question.module

        # Checks the competency score
        competency_list = []
        competency_display_list = []
        if question.a_score:
            competency_list.append("Advanced")
            competency_display_list.append(
                {"displayName": "Advanced", "score": question.a_score}
            )
        if question.c_score:
            competency_list.append("Competent")
            competency_display_list.append(
                {"displayName": "Competent", "score": question.c_score}
            )
        if question.p_score:
            competency_list.append("Proficient")
            competency_display_list.append(
                {"displayName": "Proficient", "score": question.p_score}
            )
        payload.proficiencyLevel = ";".join(competency_list)

        content = PayloadContent()
        content.difficultyScores = competency_display_list
        index = 0
        answer_id = None
        for key, option in question.options.items():
            content.options.append(
                {"content": render_options(option), "id": f"choice_{index}"}
            )
            if question.answer == key:
                answer_id = f"choice_{index}"
            index += 1
        content.question = render_question(question.content)

        scheme = PayloadMarkingScheme()
        scheme.correctAnswers.append({"id": answer_id})

        payload.content = json.dumps(asdict(content))
        payload.markingScheme = json.dumps(asdict(scheme))

        logger.info("Posting question: %s", asdict(payload))
        response = driver.session.post(self.create_api, json=asdict(payload))
        logger.info("Response %s", response)
        logger.info(response.content)

        # If response is not 200, we print out an error message
        if response.status_code != 201:
            logger.error('Error uploading question %s', question.title)
            logger.error(response.content)
            return False

        return True

    # end create_question()


# end class ActionUpload_MCQ2MySA
