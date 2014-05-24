from click.testing import CliRunner
from vl.cli import run


def test_run():
    runner = CliRunner()
    result = runner.invoke(run)
    assert result.exit_code == 0
    assert result.output == 'Welcome to VeraxLabs CLI\n'
