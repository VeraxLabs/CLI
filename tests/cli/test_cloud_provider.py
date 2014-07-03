import httpretty
import json
from click.testing import CliRunner
from vl.cli.cloud_provider import list_cloud_providers


@httpretty.activate
def test_cloud_provider_list_one():
    name = 'aws'
    output = {'name': '%s' % name, 'defaults': {'region': 'us-east-1', 'instance_type': 't1.micro'}}
    httpretty.register_uri(httpretty.GET, 'http://api.veraxlabs.com/cloud-providers/%s' % name,
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(list_cloud_providers, ['--name=%s' %name])
    assert result.exit_code == 0
    assert json.loads(result.output) == output


@httpretty.activate
def test_cloud_provider_list_all():
    output = [{'name': 'aws', 'defaults': {'region': 'us-east-1', 'instance_type': 't1.micro'}}]
    httpretty.register_uri(httpretty.GET, 'http://api.veraxlabs.com/cloud-providers',
                           body=json.dumps(output), content_type='application/json')
    runner = CliRunner()
    result = runner.invoke(list_cloud_providers, [])
    assert result.exit_code == 0
    assert json.loads(result.output) == output
