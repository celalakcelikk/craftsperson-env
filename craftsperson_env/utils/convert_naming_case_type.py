from craftsperson_env.utils.contraster import OTHER_CONFIG_NAME_TYPE_LIST, NAMING_CASE_LIST


def convert_naming_case_type(key_list: list,
                             naming_case_type: str = "upper-flat",
                             naming_case_join_type: str = "") -> str:
    """
    This function organizes items based on their naming case type.

    Parameters
    ----------
    naming_case_type: str
        This parameter gets naming case type. The default value is 'upper-flat'.
    naming_case_join_type: str
        This parameter gets join type of naming case type. The default value is ''.
    key_list: list
        This parameter retrieves environment variable keys.

    Returns
    -------
    return variable: str
        The return value is arranged by naming case type.
    """

    if naming_case_type not in OTHER_CONFIG_NAME_TYPE_LIST and naming_case_type in NAMING_CASE_LIST:
        if naming_case_type == "pascal":
            return "".join([key.capitalize() for key in key_list])

        elif naming_case_type == "camel":
            return "".join([key.lower() if key_list.index(key) == 0 else key.capitalize() for key in key_list])

        elif naming_case_type == "snake":
            return "_".join(key_list).lower()

        elif naming_case_type == "kebab":
            return "-".join(key_list).lower()

        elif naming_case_type == "flat":
            return "".join(key_list).lower()

        elif naming_case_type == "upper-flat":
            return "".join(key_list).upper()

        elif naming_case_type == "pascal-snake":
            return "_".join([key.capitalize() for key in key_list])

        elif naming_case_type == "camel-snake":
            return "_".join([key.lower() if key_list.index(key) == 0 else key.capitalize() for key in key_list])

        elif naming_case_type == "screaming-snake":
            return "_".join(key_list).upper()

        elif naming_case_type == "cobol":
            return "-".join(key_list).upper()

    else:
        if naming_case_type == "upper":
            return naming_case_join_type.join(key_list).upper()

        elif naming_case_type == "lower":
            return naming_case_join_type.join(key_list).lower()