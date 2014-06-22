import httpretty
import json
from click.testing import CliRunner
from vl.cli.user import \
    register, activate, resend_activation, login, logout,\
    forgot_password, reset_password, change_password, update


@httpretty.activate
def test_user_register():
    httpretty.register_uri(httpretty.POST, 'http://api.veraxlabs.com/users',
                           body='{"name": "PSL", "email": "psl@veraxlabs.com"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(register, ['--name=PSL', '--email=psl@veraxlabs.com', '--password=password'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"name": "PSL", "email": "psl@veraxlabs.com"}


@httpretty.activate
def test_user_activate():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.PUT, 'http://api.veraxlabs.com/users/%s/activation' % email,
                           body='{"success": "user activated"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(activate, ['--email=%s' % email, '--password=password', '--code=1234'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "user activated"}


@httpretty.activate
def test_user_resend_activation():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.POST, 'http://api.veraxlabs.com/users/%s/activation' % email,
                           body='{"success": "activation code resent"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(resend_activation, ['--email=%s' % email, '--password=password'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "activation code resent"}


@httpretty.activate
def test_user_login():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.POST, 'http://api.veraxlabs.com/users/%s/auth_token' % email,
                           body='{"auth_token": "1234"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(login, ['--email=psl@veraxlabs.com', '--password=password'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "logged in"}


@httpretty.activate
def test_user_logout():
    runner = CliRunner()
    result = runner.invoke(logout, [])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "logged out"}


@httpretty.activate
def test_user_forgot_password():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.POST, 'http://api.veraxlabs.com/users/%s/password' % email,
                           body='{"success": "password reset code sent"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(forgot_password, ['--email=%s' % email])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "password reset code sent"}


@httpretty.activate
def test_user_reset_password():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.PUT, 'http://api.veraxlabs.com/users/%s/password' % email,
                           body='{"success": "password reset"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(reset_password, ['--email=%s' % email, '--new-password=password',
                                            '--code=1234'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "password reset"}


@httpretty.activate
def test_user_change_password():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.PUT, 'http://api.veraxlabs.com/users/%s/password' % email,
                           body='{"success": "password changed"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(change_password, ['--email=%s' % email, '--old-password=password',
                                             '--new-password=password'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "password changed"}


@httpretty.activate
def test_user_update():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.PATCH, 'http://api.veraxlabs.com/users/%s' % email,
                           body='{"name": "Prashant", "email": "singhal.p1@gmail.com"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(update, ['--email=%s' % email, '--password=password',
                                    '--new-name=Prashant', '--new-email=singhal.p1@gmail.com'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"name": "Prashant", "email": "singhal.p1@gmail.com"}
