from click.testing import CliRunner
from vl import __version__ as vl_version
from vl.cli.main import run


def test_run():
    runner = CliRunner()
    result = runner.invoke(run, ['--version'])
    assert result.exit_code == 0
    assert result.output == 'version %s\n' % vl_version
