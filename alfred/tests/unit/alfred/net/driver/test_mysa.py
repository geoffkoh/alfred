# Standard imports
import logging
import json
from pathlib import Path
import os

# Third party imports

# Application imports
from alfred.net.driver.mysa import parse_assessment_filter, parse_qtype_fullname


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
    assert result.module_assessment_map == {
        ('A3079C', 'CW1'): {
            'CET (AY2022 Term 4)': (
                'e6ce681e-9dae-40a9-9ba6-5be34713962f',
                '19fd8729-8da5-4deb-81b1-5deeb018b0ec'
            )
        },
        ('A3079C', 'CWF'): {
            'CET (AY2022 Term 4)': (
                'e6ce681e-9dae-40a9-9ba6-5be34713962f',
                '93a8a05d-5079-4127-977b-bfacb8d91d4b'
            )
        }
    }

    # Case 2: Parse one with makeup
    data_filename = os.path.join(
        Path(__file__).parents[4],
        "resources",
        "alfred",
        "net",
        "driver",
        "assessment_filter_makeup.json",
    )
    with open(data_filename) as file:
        data = json.load(file)

    result = parse_assessment_filter(data=data)
    assert ('A3289C', 'EXM1') in result.module_assessment_map
    assert ('A3289C', 'EXM1 (Make-up)') in result.module_assessment_map

# end test_parse_assessment_filter()


def test_parse_qtype_fullname():
    """ Tests the function parse_qtype_fullname """

    # Case 1: Normal case
    fullname = "A1159C - Main<br />CET (AY2023 Term 2)"
    qtype = parse_qtype_fullname(fullname=fullname)
    assert qtype == 'CET (AY2023 Term 2)'

    # Case 2: Cannot find qtype
    fullname = "A1159C - Main"
    qtype = parse_qtype_fullname(fullname=fullname)
    assert qtype is None

    # Case 3: Another br
    fullname = "A1159C - Main<br/>CET (AY2023 Term 2)"
    qtype = parse_qtype_fullname(fullname=fullname)
    assert qtype == 'CET (AY2023 Term 2)'
