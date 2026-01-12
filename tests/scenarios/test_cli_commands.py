
import pytest
from typer.testing import CliRunner
from app.cli import app
import os
import shutil
from pathlib import Path

runner = CliRunner()

def test_init_command():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--name", "test-project"])
        assert result.exit_code == 0
        assert "Initializing new revamp project: test-project" in result.stdout
        
        assert os.path.exists("pyproject.toml")
        assert os.path.exists(".env.example")
        assert os.path.exists("README.md")
        assert os.path.exists("app")
        assert os.path.exists("prompts")
        assert os.path.exists("tests")

def test_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "revamp" in result.stdout
    assert "analyze" in result.stdout
    assert "generate" in result.stdout
    assert "init" in result.stdout
    assert "test" in result.stdout
    assert "deploy" in result.stdout
