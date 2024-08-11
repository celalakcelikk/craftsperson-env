from craftsperson_env.utils.contraster import CONFIG_FILE_TYPE_LIST, NAMING_CASE_LIST, OTHER_CONFIG_NAME_TYPE_LIST


class Checker:

    @staticmethod
    def __checker(condition_result: bool, error_message: str):
        assert condition_result, error_message

    def check_config_type(self, file_path: str) -> None:
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
        true_config_file_list_sum = sum([file_path.endswith(end_type) for end_type in CONFIG_FILE_TYPE_LIST])
        is_config_file_true = true_config_file_list_sum == 1

        error_message = (f"Enter a config type that is not valid. Approved config types include: "
                         f"{', '.join(CONFIG_FILE_TYPE_LIST)}")

        self.__checker(condition_result=is_config_file_true,
                       error_message=error_message)

    def check_naming_case_type(self, naming_case_type: str) -> None:
        """
        This function checks naming case types.

        Parameters
        ----------
        naming_case_type: str
            This parameter accepts naming case types and other configuration name types, including pascal, camel,
                snake, kebab, flat, upper-flat, pascal-snake, camel-snake, screaming-snake, cobol, upper or lower.

        Returns
        -------
        None.
        """
        case_list = NAMING_CASE_LIST + OTHER_CONFIG_NAME_TYPE_LIST
        is_naming_case_type_true = naming_case_type in case_list

        error_message = f"Enter a case type that is not valid. Approved case types: {', '.join(case_list)}"

        self.__checker(condition_result=is_naming_case_type_true,
                       error_message=error_message)
