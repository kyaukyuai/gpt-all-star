from unittest.mock import mock_open, patch

import pytest
import yaml

from gpt_all_star.helper.config_loader import load_configuration


def test_load_configuration_file_exists():
    # Create a sample YAML configuration
    yaml_config = """
key1: value1
key2:
  subkey1: subvalue1
  subkey2: subvalue2
"""

    # Mock the file opening and reading process
    with patch("builtins.open", mock_open(read_data=yaml_config)):
        with patch("os.path.exists", return_value=True):
            config = load_configuration("test_config.yaml")

    # Assert the loaded configuration
    assert config == {
        "key1": "value1",
        "key2": {"subkey1": "subvalue1", "subkey2": "subvalue2"},
    }


def test_load_configuration_file_not_exists():
    # Mock the os.path.exists function to return False
    with patch("os.path.exists", return_value=False):
        config = load_configuration("nonexistent_config.yaml")

    # Assert that an empty dictionary is returned when the file doesn't exist
    assert config == {}


def test_load_configuration_invalid_yaml():
    # Create an invalid YAML configuration
    invalid_yaml_config = """
key1: value1
  invalid_indent: value2
"""

    # Mock the file opening and reading process
    with patch("builtins.open", mock_open(read_data=invalid_yaml_config)):
        with patch("os.path.exists", return_value=True):
            # Assert that a YAMLError is raised when loading an invalid YAML file
            with pytest.raises(yaml.YAMLError):
                load_configuration("invalid_config.yaml")
