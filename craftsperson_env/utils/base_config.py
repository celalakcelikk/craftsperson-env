"""
This file is metaclass file of other classes.
"""

from craftsperson_env.utils.assert_controller import Checker
class BaseConfigClass:
    """
    Task
    ----
    BaseConfigClass metaclass for subclasses.
    When add this class as metaclass to any subclass, each subclasses will have following attrs as default.

    Parameters
    ----------
    None.

    Returns
    -------
    None.

    Examples:
    --------
    None.
    """

    def __new__(cls, *args, **kwargs):
        """
        Task
        ----
        Create and return a new instance of the class.

        Parameters
        ----------
        *args : tuple
           Positional arguments passed to the constructor.
        **kwargs : dict
           Keyword arguments passed to the constructor.

        Returns
        -------
        instance : object
           The newly created instance of the class.
        """
        instance = super().__new__(cls, *args, **kwargs)

        instance.naming_case_type = "upper-flat"
        instance.naming_case_join_type = ""
        instance.checker = Checker()
        return instance
