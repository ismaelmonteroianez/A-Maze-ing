"""
Custom exceptions for configuration parsing and validation errors.

This module defines specific exceptions used throughout the project
to handle configuration-related errors in a clear and structured way.
"""


class InvalidConfiguration(Exception):
    """
    Exception raised when the configuration file contains invalid values.
    This includes malformed parameters, out-of-range values, or
    logically inconsistent configuration settings.
    """
    pass


class EmptyFile(Exception):
    """
    Exception raised when the configuration file is empty.
    Used to prevent the program from running without valid input data.
    """
    pass
