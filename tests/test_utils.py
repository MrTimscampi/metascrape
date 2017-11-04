import pytest
from meta_scrape import utils


def test_clean_title():
    assert utils.clean_title("test [DVD]") == "test"
    assert utils.clean_title("test [Blu-ray]") == "test"
    assert utils.clean_title("test　space") == "test space"
    assert utils.clean_title("test Blu-ray版") == "test"
    assert utils.clean_title("test DVD版") == "test"
    assert utils.clean_title("test 【特価】") == "test"
    assert utils.clean_title("test【10%POINTBACK】") == "test"
