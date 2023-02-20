""" Action for uploading questions """

# Standard import
from dataclasses import asdict, dataclass, field
import json
import logging
from typing import Dict, List

# Application import
from alfred.net.driver.base import DriverBase
from alfred.io.question import QuestionBank, MultipleChoiceQuestion

logger = logging.getLogger(__name__)


@dataclass
class Payload:
    """This is the payload to send to the API for creating a question"""

    topics: List[str] = field(default_factory=list)
    title: str = None
    type: int = 0
    selectedType: Dict = field(default_factory=dict)
    disabled: bool = False
    question: str = None
    score: int = 0
    moduleCode: str = "-1"
    lessonCode: str = "-1"
    hint: str = ""
    explanation: str = ""
    resources: List[str] = field(default_factory=list)
    content: str = None
    subQuestions: List[str] = field(default_factory=list)
    subQuestionOrder: str = None
    addToBoth: bool = False
    addToPersonal: bool = True
    addToModule: bool = False
    isDuplicate: bool = False
    bankType: int = 1
    proficiencyLevel: int = 0
    moduleName: str = "None"
    lessonName: str = "None"


@dataclass
class PayloadContent:
    """Content portion of the payload"""

    responseIdentifier: str = "Response"
    scoreType: str = "0"
    shuffle: bool = False
    displayType: int = 1
    choiceItems: List = field(default_factory=list)


@dataclass
class ChoiceItem:
    """Choice items"""

    id: str = None
    answer: str = None
    isCorrect: bool = False


class ActionUpload_MCQ2MyLEO:
    """Action class for uploading question"""

    def __init__(self):
        """Constructor"""
        self.url = "https://myleo.rp.edu.sg/Quiz/QuestionBank/QuestionList"
        self.create_api = "https://myleo.rp.edu.sg/Quiz/api/Question/CreateQuestion"

    # end __init__()

    def run(self, driver: DriverBase, bank: QuestionBank):
        """Runs this particular action"""

        logger.info("Creating questions")
        counter = 0
        for question in bank.questions:
            if self.create_question(driver=driver, question=question):
                counter += 1
        logger.info("%s/%s Questions created", counter, len(bank.questions))
        driver.navigate(self.url)

    # end run()

    def create_question(self, driver: DriverBase, question: MultipleChoiceQuestion):
        """Creates a multiple choice question"""

        logger.info("Creating question: %s", question.title)

        payload = Payload()
        payload.title = question.title
        payload.question = question.content
        payload.selectedType = {
            "name": "Multiple Choice",
            "value": 0,
            "isChecked": True,
        }
        payload.score = int(question.score)
        payload.question = question.content

        counter = 1
        payload_content = PayloadContent()
        for option, option_desc in question.options.items():
            item = ChoiceItem(
                id=f"choice_{counter}",
                answer=option_desc,
                isCorrect=option == question.answer,
            )
            payload_content.choiceItems.append(asdict(item))
            counter += 1

        payload.content = json.dumps(asdict(payload_content))

        logger.info("Posting question: %s", asdict(payload))
        response = driver.session.post(self.create_api, data=asdict(payload))
        logger.info("Response %s", response)
        logger.info(response.content)

        # If response is not 200, we print out an error message
        if response.status_code != 200:
            logger.error('Error uploading question %s', question.title)
            logger.error(response.content)
            return False
        
        return True

    # end create_question()


# end class ActionUpload_MCQ2MyLEO
