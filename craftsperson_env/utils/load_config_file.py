import json

import toml
import xmltodict


class LoadConfigFile:

    @staticmethod
    def load_diff_type_env_config_file(file_path: str,
                                       config_env_replace_first_value: str,
                                       naming_case_join_type: str):
        """
        This function loads env file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.
        naming_case_join_type: str
            This parameter gets join type of naming case type.
        config_env_replace_first_value: str
            This parameter gets replacing first value on config_env variables.

        Returns
        -------
        config_dict: dict
            This parameter return changing naming case on variables of config file.
        """
        with open(file_path, "r") as f:
            config_env = f.read().strip().split("\n")

        config_dict = {}
        for c in config_env:
            split_list = c.split("=")
            key = split_list[0].replace(config_env_replace_first_value,
                                        naming_case_join_type) \
                if config_env_replace_first_value is not None else split_list[0]
            value = split_list[1]
            config_dict[key] = value

        return config_dict

    @staticmethod
    def load_json_config_file(file_path: str):
        """
        This function loads json file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.

        Returns
        -------
        config_dict: dict
            This parameter return variables of config file.
        """
        with open(file_path, 'r') as file:
            config_dict = json.load(file)

        return config_dict

    @staticmethod
    def load_xml_config_file(file_path: str,
                             extra_config_file_params: dict = {}):
        """
        This function loads xml file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.
        extra_config_file_params: dict
            This parameter gets xml file extra dict type config.

        Returns
        -------
        config_dict: dict
            This parameter return variables of config file.
        """
        with open(file_path, 'r') as file:
            config_dict = xmltodict.parse(file.read(), **extra_config_file_params)

        return config_dict

    @staticmethod
    def load_toml_config_file(file_path: str,
                              extra_config_file_params: dict = {}):
        """
        This function loads toml file to the 'os.environ' system.

        Parameters
        ----------
        file_path: str
            This parameter specifies the file location path.
        extra_config_file_params: dict
            This parameter gets xml file extra dict type config.
        Returns
        -------
        None.
        config_dict: dict
            This parameter return variables of config file.
        """
        with open(file_path, 'r') as file:
            config_dict = toml.load(file, **extra_config_file_params)

        return config_dict
