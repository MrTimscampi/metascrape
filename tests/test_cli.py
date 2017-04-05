import pytest
from click.testing import CliRunner
from meta_scrape import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert not result.exception


def test_cli_with_arg(runner):
    result = runner.invoke(cli.main, ['list-scrapers'])
    assert result.exit_code == 0
    assert not result.exception
    assert "EIC-Book" in result.output.strip()
