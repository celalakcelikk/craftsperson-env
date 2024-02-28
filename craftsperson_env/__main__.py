"""
This file serves as the main class.
"""
import json
import os
from typing import Any

import toml
import validators
import xmltodict
import yaml
from dotenv import load_dotenv

from craftsperson_env.utils.contraster import CONFIG_FILE_TYPE_LIST, NAMING_CASE_LIST, OTHER_CONFIG_NAME_TYPE_LIST


class CraftsEnvConfig:
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
        self.__naming_case_type = "upper-flat"
        self.__naming_case_join_type = ""
        self.__is_remove_xml_first_level = False
        self.__is_change_config_env_format = False
        self.__config_env_replace_first_value = None
        self.__extra_config_file_params = {}

    @staticmethod
    def __check_config_type(file_path: str) -> None:
        """
        This function checks the config file's end-type.

        Parameters
        ----------
        file_path: str
            This parameter accepts a file location path in env, yaml, json, xml, or toml formats.

        Returns
        -------
        None.
        """
        is_config_file_true = sum([file_path.endswith(end_type) for end_type in CONFIG_FILE_TYPE_LIST])
        assert is_config_file_true == 1, \
            f"Enter a config type that is not valid. Approved config types include: {', '.join(CONFIG_FILE_TYPE_LIST)}"

    @staticmethod
    def __check_naming_case_type(naming_case_type: str) -> None:
        """
        This function checks naming case types.

        Parameters
        ----------
        naming_case_type: str
            This parameter accepts naming case types and other configuration name types, including pascal, camel,
                snake, kebab, flat, upper-flat, pascal-snake, camel-snake, screaming-snake,
                train, cobol, upper or lower.

        Returns
        -------
        None.
        """
        case_list = NAMING_CASE_LIST + OTHER_CONFIG_NAME_TYPE_LIST
        is_naming_case_type_true = naming_case_type in case_list
        assert is_naming_case_type_true is True, \
            f"Enter a case type that is not valid. Approved case types: {', '.join(case_list)}"

    @staticmethod
    def __add_base_path(file_path: str, root_full_path: str) -> str:
        """
        This function adds a full path to the config file.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.
        root_full_path: str
            This parameter retrieves the full path for the file.

        Returns
        -------
        file_path: str
            The return value is a complete path generated by combining the file_path and root_full_path parameters.
        """
        if validators.url(file_path) is False:
            if file_path.startswith("./"):
                file_path = file_path.replace('./', root_full_path + '/')
            else:
                file_path = f"{root_full_path}/{file_path}"

        return file_path

    def __arrangement_naming_case_type(self, key_list: list) -> str:
        """
        This function organizes items based on their naming case type.

        Parameters
        ----------
        key_list: list
            This parameter retrieves environment variable keys.

        Returns
        -------
        return variable: str
            The return value is arranged by naming case type.
        """
        if self.__naming_case_type not in OTHER_CONFIG_NAME_TYPE_LIST and self.__naming_case_type in NAMING_CASE_LIST:
            if self.__naming_case_type == "pascal":
                return "".join([key.capitalize() for key in key_list])

            elif self.__naming_case_type == "camel":
                return "".join([key.lower() if key_list.index(key) == 0 else key.capitalize() for key in key_list])

            elif self.__naming_case_type == "snake":
                return "_".join(key_list).lower()

            elif self.__naming_case_type == "kebab":
                return "-".join(key_list).lower()

            elif self.__naming_case_type == "flat":
                return "".join(key_list).lower()

            elif self.__naming_case_type == "upper-flat":
                return "".join(key_list).upper()

            elif self.__naming_case_type == "pascal-snake":
                return "_".join([key.capitalize() for key in key_list])

            elif self.__naming_case_type == "camel-snake":
                return "_".join([key.lower() if key_list.index(key) == 0 else key.capitalize() for key in key_list])

            elif self.__naming_case_type == "screaming-snake":
                return "_".join(key_list).upper()

            elif self.__naming_case_type == "train":
                return "-".join([key.capitalize() for key in key_list])

            elif self.__naming_case_type == "cobol":
                return "-".join(key_list).upper()

        else:
            if self.__naming_case_type == "upper":
                return self.__naming_case_join_type.join(key_list).upper()

            elif self.__naming_case_type == "lower":
                return self.__naming_case_join_type.join(key_list).lower()

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
                env_key = self.__arrangement_naming_case_type(key_list=key_list)

                if isinstance(value, dict):
                    os.environ[env_key] = f'"{value}"'

                else:
                    os.environ[env_key] = f'{value}'

    def __load_env_config_file(self, file_path: str):
        """
        This function loads env file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.

        Returns
        -------
        None.
        """
        if self.__is_change_config_env_format:
            with open(file_path, "r") as f:
                config_env = f.read().strip().split("\n")

            config_dict = {}
            for c in config_env:
                split_list = c.split("=")
                key = split_list[0].replace(self.__config_env_replace_first_value,
                                            self.__naming_case_join_type) \
                    if self.__config_env_replace_first_value is not None else split_list[0]
                value = split_list[1]
                config_dict[key] = value

            self.__add_config_env(config_dict)

        else:
            load_dotenv(file_path)

    def __load_yaml_config_file(self, file_path: str):
        """
        This function loads yaml file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.

        Returns
        -------
        None.
        """
        with open(file_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        self.__add_config_env(config_dict)

    def __load_json_config_file(self, file_path: str):
        """
        This function loads json file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.

        Returns
        -------
        None.
        """
        with open(file_path, 'r') as file:
            config_dict = json.load(file)
        self.__add_config_env(config_dict)

    def __load_xml_config_file(self, file_path: str):
        """
        This function loads xml file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.

        Returns
        -------
        None.
        """
        with open(file_path, 'r') as file:
            config_dict = xmltodict.parse(file.read(), **self.__extra_config_file_params)
        self.__add_config_env(config_dict)

    def __load_toml_config_file(self, file_path: str):
        """
        This function loads toml file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.

        Returns
        -------
        None.

        """
        with open(file_path, 'r') as file:
            config_dict = toml.load(file, **self.__extra_config_file_params)
        self.__add_config_env(config_dict)

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
        self.__check_config_type(file_path=file_path)
        file_path = self.__add_base_path(file_path=file_path, root_full_path=root_full_path)
        self.__check_naming_case_type(naming_case_type=naming_case_type)

        self.__naming_case_type = naming_case_type
        self.__naming_case_join_type = naming_case_join_type
        self.__is_change_config_env_format = is_change_config_env_format
        self.__config_env_replace_first_value = config_env_replace_first_value
        self.__is_remove_xml_first_level = is_remove_xml_first_level
        self.__extra_config_file_params = extra_config_file_params

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
    def get(key: str, value_type: Any = str, default: Any = None) -> str:
        """
        This function retrieves the value associated with the key from the 'os.environ' system.

        Parameters
        ----------
        key: str
            This parameter retrieves the key from the 'os.environ' system.
        value_type: str, optional.
            This parameter accepts value types such as int, str, list, dict, and others. The default value is str.
        default: Any, optional.
            This parameter retrieves the default value if the key is not found in any environment variables.
                The default is None.

        Returns
        -------
        value:
            This returns the value of the given environment variable key.
        """
        value = os.getenv(key, default)
        value_type = json.loads if value_type == dict and (
                default not in [{}, None] or value not in [{}, None]) else value_type

        if value is None:
            value = None

        elif value_type != list:
            value = value_type(value)

        try:
            value = eval(value)

        except Exception:
            pass

        return value

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
