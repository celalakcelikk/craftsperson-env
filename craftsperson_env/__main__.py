"""
This file serves as the main class.
"""
import json
import os
from typing import Any

import toml
import xmltodict
import yaml
from dotenv import load_dotenv

from craftsperson_env.utils.base_config import BaseConfigClass
from craftsperson_env.utils.convert_naming_case_type import convert_naming_case_type
from craftsperson_env.utils.pather import add_base_path


class CraftsEnvConfig(BaseConfigClass):
    """
    Task
    ----
    This class serves as an environment variable parser.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """

    def __init__(self):
        self.__is_remove_xml_first_level = False
        self.__is_change_config_env_format = False
        self.__config_env_replace_first_value = None
        self.__extra_config_file_params = {}

    def __add_config_env(self, data: Any, keys: list = []):
        """
        This function adds config file key-value pairs to the 'os.environ' system.

        Parameters
        ----------
        data : Any
            This parameter retrieves environment variable values.
        keys : list, optional
            This parameter retrieves the list of environment variable keys. The default value is [].

        Returns
        -------
        None.
        """
        for key, value in data.items():
            key_list = keys + [key]

            if isinstance(value, str):
                try:
                    value = eval(value)
                    is_dict_value = True
                except Exception:
                    is_dict_value = False
            else:
                is_dict_value = False

            if isinstance(value, dict) and is_dict_value is False:
                self.__add_config_env(value, key_list)

            else:
                key_list = key_list[1:] if self.__is_remove_xml_first_level else key_list
                env_key = convert_naming_case_type(key_list=key_list,
                                                   naming_case_type=self.naming_case_type,
                                                   naming_case_join_type=self.naming_case_join_type)

                if isinstance(value, dict):
                    os.environ[env_key] = f'"{value}"'

                else:
                    os.environ[env_key] = f'{value}'


    def load_config_file(self,
                         file_path: str,
                         root_full_path: str = "./",
                         naming_case_type: str = None,
                         naming_case_join_type: str = "",
                         is_change_config_env_format: bool = False,
                         config_env_replace_first_value: str = None,
                         is_remove_xml_first_level: bool = False,
                         extra_config_file_params: dict = {}):
        """
        This function processes and uses a config file.

        Parameters
        ----------
        file_path : str
            This parameter specifies the file location path.
        root_full_path : str, optional
            This parameter retrieves the full path from the file. The default is './'.
        naming_case_type : str, optional
            This parameter specifies naming case types for env, yaml, json, xml, or toml. The default is None.
        naming_case_join_type : str, optional.
            This parameter specifies the join type, allowing values such as "", "-", or "_". The default is "".
        is_change_config_env_format: bool, optional.
            This parameter specifies whether the format of the env config file has been changed.
                The default value is False.
        config_env_replace_first_value: str, optional.
            This parameter specifies the replacement value for the first occurrence. The default is None.
        is_remove_xml_first_level : bool, optional
            This parameter determines whether to remove the first level. The default value is False.
        extra_config_file_params : dict, optional
            This parameter retrieves additional XML or TOML configuration parameters. The default value is {}.

        Returns
        -------
        None.
        """
        self.checker.check_config_type(file_path=file_path)
        self.checker.check_naming_case_type(naming_case_type=naming_case_type)
        file_path = add_base_path(file_path=file_path, root_full_path=root_full_path)

        is_change_config_env_format = is_change_config_env_format
        config_env_replace_first_value = config_env_replace_first_value
        is_remove_xml_first_level = is_remove_xml_first_level
        extra_config_file_params = extra_config_file_params

        if file_path.endswith("env"):
            self.__is_remove_xml_first_level = False
            self.__load_env_config_file(file_path=file_path)

        elif file_path.endswith("yaml"):
            self.__is_remove_xml_first_level = False
            self.__load_yaml_config_file(file_path=file_path)

        elif file_path.endswith("json"):
            self.__is_remove_xml_first_level = False
            self.__load_json_config_file(file_path=file_path)

        elif file_path.endswith("xml"):
            self.__load_xml_config_file(file_path=file_path)

        elif file_path.endswith("toml"):
            self.__is_remove_xml_first_level = False
            self.__load_toml_config_file(file_path=file_path)

    @staticmethod
    def get(key: str, value_type: Any = str, default: Any = None) -> Any:
        """
        This function retrieves the value associated with the key from the 'os.environ' system.

        Parameters
        ----------
        key: str
            This parameter retrieves the key from the 'os.environ' system.
        value_type: Any, optional.
            This parameter accepts value types such as int, str, float, list, dict, bool and others.
            The default value is str.
        default: Any, optional.
            This parameter retrieves the default value if the key is not found in any environment variables.
                The default is None.

        Returns
        -------
        value: Any
            This returns the value of the given environment variable key with the specified type.
        """
        value = os.getenv(key, None)

        # Return default if key not found
        if value is None:
            return default

        # Type conversion based on value_type
        if value_type == dict:
            try:
                # Handle both single and double quotes in JSON strings
                json_value = value.strip().strip('"').strip("'")
                return json.loads(json_value.replace("'", '"'))
            except (json.JSONDecodeError, AttributeError):
                return default

        elif value_type == float:
            try:
                return float(value)
            except (ValueError, TypeError):
                return default

        elif value_type == int:
            try:
                return int(float(value))  # Handle "2.0" -> 2
            except (ValueError, TypeError):
                return default

        elif value_type == bool:
            if isinstance(value, bool):
                return value
            return str(value).lower() in ('true', '1', 'yes')

        elif value_type == list:
            try:
                json_value = value.strip().strip('"').strip("'")
                return json.loads(json_value.replace("'", '"'))
            except (json.JSONDecodeError, AttributeError):
                # Fallback: split by comma
                return [item.strip() for item in value.split(',')]

        elif value_type == str:
            return str(value)

        # For any other type, try direct conversion
        try:
            return value_type(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        This function sets a key-value pair in the 'os.environ' system.

        Parameters
        ----------
        key: str
            This parameter specifies the key to be set as an environment variable.
        value: str
            This parameter specifies the value that will be stored in
                the environment variable identified by the given key.

        Returns
        -------
        None.
        """
        os.environ[key] = str(value)
