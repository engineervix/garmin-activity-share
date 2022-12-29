#!/usr/bin/env python3

import pytest

from garmin_activity_share.garmin_connect import sum


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests

    return requests.get("https://github.com/engineervix/garmin-activity-share")


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    from bs4 import BeautifulSoup

    assert "GitHub" in BeautifulSoup(response.content, "html.parser").title.string


def test_sum():
    assert sum(2, 3) == 5
