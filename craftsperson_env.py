"""
This file is the system configuration settings.
"""
import json
import os
from typing import Any
import toml
import validators
import xmltodict
import yaml
from dotenv import load_dotenv
from utils.contraster import CONFIG_FILE_TYPE_LIST, CONFIG_CASE_LIST


class CraftsPersonEnvConfigHandler:
    """
    Task
    ----
    Environment variable parser.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """

    def __init__(self):
        self.__case_type = "upper-flat"

    @staticmethod
    def __check_config_type(file_path):
        is_config_file_true = sum([file_path.endswith(end_type) for end_type in CONFIG_FILE_TYPE_LIST])
        assert is_config_file_true == 1, \
            f"Enter a config type that is not valid. Approved config types: {', '.join(CONFIG_FILE_TYPE_LIST)}"

    @staticmethod
    def __check_case_type(case_type):
        is_case_type_true = sum([case_type.endswith(end_type) for end_type in CONFIG_CASE_LIST])
        assert is_case_type_true == 1, \
            f"Enter a case type that is not valid. Approved case types: {', '.join(CONFIG_CASE_LIST)}"

    @staticmethod
    def __add_base_path(file_path: str, base_dir: str):
        if validators.url(file_path) is False:
            if file_path.startswith("./"):
                file_path = file_path.replace('./', base_dir + '/')
            else:
                file_path = f"{base_dir}/{file_path}"

        return file_path

    def __choice_case_type(self, key_list):

        if self.__case_type == "pascal":
            return "".join([key.capitalize() for key in key_list])

        elif self.__case_type == "camel":
            return "".join([key.lower() if key_list.index(key) == 0 else key.capitalize() for key in key_list])

        elif self.__case_type == "snake":
            return "_".join(key_list).lower()

        elif self.__case_type == "kebab":
            return "-".join(key_list).lower()

        elif self.__case_type == "kebab":
            return "".join(key_list).lower()

        elif self.__case_type == "upper-flat":
            return "".join(key_list).upper()

        elif self.__case_type == "pascal-snake":
            return "_".join([key.capitalize() for key in key_list])

        elif self.__case_type == "camel-snake":
            return "_".join([key.lower() if key_list.index(key) == 0 else key.capitalize() for key in key_list])

        elif self.__case_type == "screaming-snake":
            return "_".join(key_list).upper()

        elif self.__case_type == "train":
            return "-".join([key.capitalize() for key in key_list])

        elif self.__case_type == "cobol":
            return "-".join(key_list).upper()

    def __add_config_env(self, data, keys=None):
        if keys is None:
            keys = []

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
                env_key = self.__choice_case_type(key_list=key_list)

                if isinstance(value, dict):
                    os.environ[env_key] = f'"{value}"'

                else:
                    os.environ[env_key] = f'{value}'

    def __use_xml_config_file(self, file_path: str):
        with open(file_path, 'r') as file:
            config_dict = xmltodict.parse(file)
        self.__add_config_env(config_dict)

    def __use_toml_config_file(self, file_path: str):
        with open(file_path, 'r') as file:
            config_dict = toml.load(file)
        self.__add_config_env(config_dict)

    def __use_json_config_file(self, file_path: str):
        with open(file_path, 'r') as file:
            config_dict = json.load(file)
        self.__add_config_env(config_dict)

    @staticmethod
    def __use_env_config_file(file_path: str):
        load_dotenv(file_path)

    def __use_yaml_config_file(self, file_path: str):
        with open(file_path, 'r') as file:
            config_dict = yaml.safe_load(file)

        self.__add_config_env(config_dict)

    def use_config_file(self, file_path: str, base_dir: str = "./", case_type: str = "upper-flat"):
        self.__check_config_type(file_path=file_path)
        file_path = self.__add_base_path(file_path=file_path, base_dir=base_dir)

        self.__check_case_type(case_type=case_type)
        self.__case_type = case_type

        if file_path.endswith("env"):
            self.__use_env_config_file(file_path=file_path)

        elif file_path.endswith("yaml"):
            self.__use_yaml_config_file(file_path=file_path)

        elif file_path.endswith("json"):
            self.__use_json_config_file(file_path=file_path)

        elif file_path.endswith("xml"):
            self.__use_xml_config_file(file_path=file_path)

        elif file_path.endswith("toml"):
            self.__use_toml_config_file(file_path=file_path)

    @staticmethod
    def get(key: str, value_type: Any = str, default: Any = None) -> str:
        """
        Task
        ----
        Call when object itself has request to get environment variable with/without defining class instance.

        Parameters
        ----------
        value_type: str
        key: str
            Default value if key does not found int environment variables.
        default: str
            Default value if key does not found int environment variables.

        Returns
        -------
        Value of given environment variable key.

        Examples
        --------
        >>> import os
        >>> ConfigHanler.get('test_get')
        'test-value'
        >>> ConfigHanler.get('test_not_exists_key')
        >>> ConfigHanler.get('test_not_exists_key', default='a default test value')
        'a default test value'
        """
        value = os.getenv(key, default)
        value_type = json.loads if value_type == dict and (
                default not in [{}, None] or value not in [{}, None]) else value_type
        value = None if value is None else value_type(value)
        return value

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Task
        ----
        Call when request to set an environment variables with/without defining class instance.

        Parameters
        ----------
        key: str
            The key you want to set as environment variable.
        value: str
            Value to be stored in given environment variable with given key.

        Returns
        -------
        None.

        Examples
        --------
        >>> config = ConfigHanler()
        >>> Config.set('test_set', 'test-value')
        >>> import os; os.getenv('test_set')
        'test-value'
        """

        os.environ[key] = value
