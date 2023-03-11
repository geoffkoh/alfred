# Standard imports
import logging
import json
from pathlib import Path
import os

# Third party imports

# Application imports
from alfred.net.driver.mysa import parse_assessment_filter


def test_parse_assessment_filter():
    """Test the function parse_assessment_filter"""

    data_filename = os.path.join(
        Path(__file__).parents[4],
        "resources",
        "alfred",
        "net",
        "driver",
        "assessment_filter.json",
    )
    with open(data_filename) as file:
        data = json.load(file)

    result = parse_assessment_filter(data=data)
    assert result.module_assessment_pairmap == {
        ('A3079C', 'CW1'): (
            'e6ce681e-9dae-40a9-9ba6-5be34713962f',
            '19fd8729-8da5-4deb-81b1-5deeb018b0ec'
        ),
        ('A3079C', 'CWF'): (
            'e6ce681e-9dae-40a9-9ba6-5be34713962f',
            '93a8a05d-5079-4127-977b-bfacb8d91d4b'
        )
    }

# end test_parse_assessment_filter()
