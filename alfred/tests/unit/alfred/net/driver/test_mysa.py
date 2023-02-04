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
        ("A1119C", "CWF"): (
            "1d3dbffd-3eda-4f8b-8273-3a5606f84bb1",
            "ea159962-b7da-4719-bb61-e589b04d9f74",
        ),
        ("A1129C", "CWF"): (
            "e07fcfe3-ed6a-45ed-9fe9-87f808691873",
            "ce5b4d05-9141-4a4d-97dc-3403fa39a269",
        ),
        ("A1139C", "CWF"): (
            "c2068fc3-4d8c-4edf-acb6-95fa51f7bc7b",
            "721584e9-8b92-47b1-85a3-04cf14b28942",
        ),
        ("A1149C", "CWF"): (
            "98e34aef-158e-4632-92b4-705774325f27",
            "8458b5b1-f927-4a5d-b4a8-83dc4362bc61",
        ),
        ("A2009C", "CWF"): (
            "cee352c8-d74d-424b-bee6-3fb89190ab08",
            "c1613143-12cb-4446-983d-2d9aef45e59d",
        ),
        ("A2019C", "CWF"): (
            "218d8998-00f1-471b-9db8-dfde21b3cc22",
            "9ab2683c-784b-46c0-a975-93afcd441551",
        ),
        ("A2129C", "CWF"): (
            "b56587ce-9759-4490-ae3a-e97d8758313a",
            "71f0a8fb-9164-44b8-a1dc-b8642143d9b4",
        ),
        ("A3079C", "CW1"): (
            "e6ce681e-9dae-40a9-9ba6-5be34713962f",
            "19fd8729-8da5-4deb-81b1-5deeb018b0ec",
        ),
        ("A3079C", "CWF"): (
            "e6ce681e-9dae-40a9-9ba6-5be34713962f",
            "93a8a05d-5079-4127-977b-bfacb8d91d4b",
        ),
        ("A1159C", "CWF"): (
            "1c9fcaab-2b16-43c5-87c3-7449b852bb71",
            "3447c693-8dee-4f9b-987c-f08111632715",
        ),
        ("A1169C", "CWF"): (
            "8bf68ddf-01f5-4ce1-a150-82d170c87c2c",
            "8db4676a-07e3-4598-8711-d5ea7ddbf199",
        ),
        ("A1189C", "CWF"): (
            "a9c541c1-880c-4d9f-aff1-96bedb13d429",
            "a0e4371b-6d3e-4b16-b5ad-6b6d56ab5810",
        ),
        ("A2069C", "CWF"): (
            "08884503-ecd1-4d27-bbf2-46217c46bafe",
            "9c4a65e5-9186-461b-9bb2-0fd72cdaae63",
        ),
        ("A3059C", "CWF"): (
            "52dbc2e4-6d51-45a1-a8db-2e938c29c775",
            "d6d657c0-a05b-46b2-b737-b8f1139c2f70",
        ),
        ("A0001F", "CA1"): (
            "233f1b7f-965f-4df7-a810-08d8fb311d52",
            "b4a602fe-1f38-44f2-9cc2-211705b502ef",
        ),
        ("A0001F", "CA3"): (
            "19e66bde-2c5c-4863-84e6-4e1e2bd06d6d",
            "80140c18-64cf-4ef9-87e1-73623190cce1",
        ),
        ("A0001F", "CA2"): (
            "19e66bde-2c5c-4863-84e6-4e1e2bd06d6d",
            "4ac2d78b-1f2c-4706-adc1-32117123c412",
        ),
        ("A0001F", "Supplementary Exam"): (
            "19e66bde-2c5c-4863-84e6-4e1e2bd06d6d",
            "1a4d3e5f-a98d-43ff-8031-a900993041d6",
        ),
    }


# end test_parse_assessment_filter()
