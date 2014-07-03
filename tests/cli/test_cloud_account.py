import httpretty
import json
from click.testing import CliRunner
from vl.cli.user import login
from vl.cli.cloud_account import add, list_cloud_accounts, update, delete


def user_login():
    email = 'psl@veraxlabs.com'
    httpretty.register_uri(httpretty.POST, 'http://api.veraxlabs.com/users/%s/auth_token' % email,
                           body='{"auth_token": "1234"}',
                           content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(login, ['--email=psl@veraxlabs.com', '--password=password'])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"success": "logged in"}


@httpretty.activate
def test_cloud_account_add():
    user_login()
    output = {'user': 'psl@veraxlabs.com', 'name': 'aws1', 'cloud_provider': 'aws',
              'api_key': '12345', 'api_secret': '98765'}
    httpretty.register_uri(httpretty.POST, 'http://api.veraxlabs.com/cloud-accounts',
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(add, ['--cloud-provider=aws', '--name=aws1', '--api-key=12345', '--api-secret=98765'])
    assert result.exit_code == 0
    assert json.loads(result.output) == output


@httpretty.activate
def test_cloud_account_list_one():
    user_login()
    name = 'aws1'
    output = {'user': 'psl@veraxlabs.com', 'name': '%s' % name, 'cloud_provider': 'aws',
              'api_key': '12345', 'api_secret': '98765'}
    httpretty.register_uri(httpretty.GET, 'http://api.veraxlabs.com/cloud-accounts/%s' % name,
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(list_cloud_accounts, ['--name=%s' % name])
    assert result.exit_code == 0
    assert json.loads(result.output) == output


@httpretty.activate
def test_cloud_account_list_all():
    user_login()
    output = [{'user': 'psl@veraxlabs.com', 'name': 'aws1', 'cloud_provider': 'aws',
               'api_key': '12345', 'api_secret': '98765'}]
    httpretty.register_uri(httpretty.GET, 'http://api.veraxlabs.com/cloud-accounts',
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(list_cloud_accounts, [])
    assert result.exit_code == 0
    assert json.loads(result.output) == output


@httpretty.activate
def test_cloud_account_update():
    user_login()
    name = 'aws1'
    output = {'user': 'psl@veraxlabs.com', 'name': 'aws2', 'cloud_provider': 'aws',
              'api_key': '98765', 'api_secret': 'qwerty'}
    httpretty.register_uri(httpretty.PATCH, 'http://api.veraxlabs.com/cloud-accounts/%s' % name,
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(update, ['--name=%s' % name, '--new-name=aws2',
                                    '--new-api-key=98765', '--new-api-secret=qwerty'])
    assert result.exit_code == 0
    assert json.loads(result.output) == output


@httpretty.activate
def test_cloud_account_delete():
    user_login()
    name = 'aws1'
    output = {'success': 'cloud account deleted'}
    httpretty.register_uri(httpretty.DELETE, 'http://api.veraxlabs.com/cloud-accounts/%s' % name,
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(delete, ['--name=%s' % name])
    assert result.exit_code == 0
    assert json.loads(result.output) == output
