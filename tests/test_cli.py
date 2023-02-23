import json
import os
import tempfile

from unittest.mock import patch

from click.testing import CliRunner
from stacklet.client.sinistral.cli import cli


def test_commands_present():
    runner = CliRunner()
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "policy" in result.output
    assert "projects" in result.output
    assert "policy-collections" in result.output
    assert "policy-sources" in result.output
    assert "scans" in result.output
    assert "group" in result.output
    assert "run" in result.output
    assert "login" in result.output
    assert "configure" in result.output
    assert "show" in result.output


def test_cli_show():
    config = {
        "api": "https://api.sinistral.acme.org",
        "region": "us-east-1",
        "cognito_client_id": "foo",
        "cognito_user_pool_id": "bar",
        "idp_id": "baz",
        "auth_url": "https://auth.sinistral.acme.org",
        "cubejs": "",
    }
    temp = tempfile.NamedTemporaryFile(delete=False)
    with open(temp.name, "w") as f:
        json.dump(config, f)
    runner = CliRunner()
    with patch.dict(os.environ, {"STACKLET_CONFIG": temp.name}):
        result = runner.invoke(cli, ["show"])
        assert result.exit_code == 0
        assert "api.sinistral.acme.org" in result.output

    os.unlink(temp.name)


def test_cli_configure():
    temp = tempfile.NamedTemporaryFile(delete=False)
    # delete the file, cli should create it for us
    os.unlink(temp.name)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "configure",
            "--api=foo",
            "--region=bar",
            "--cognito-client-id=ccid",
            "--cognito-user-pool-id=cupid",
            "--idp-id=idpid",
            "--auth-url=auth.com",
            f"--location={temp.name}",
        ],
    )
    assert result.exit_code == 0
    with open(temp.name) as f:
        res = json.load(f)
        assert res["api"] == "foo"
    os.unlink(temp.name)


def test_cli_login_cognito():
    config = {
        "api": "https://api.sinistral.acme.org",
        "region": "us-east-1",
        "cognito_client_id": "foo",
        "cognito_user_pool_id": "bar",
        "idp_id": "baz",
        "auth_url": "https://auth.sinistral.acme.org",
        "cubejs": "",
    }
    temp = tempfile.NamedTemporaryFile(delete=False)
    with open(temp.name, "w") as f:
        json.dump(config, f)
    runner = CliRunner()
    runner.invoke(cli, ["login", "--username=foo", "--password=bar"])
    os.unlink(temp.name)
