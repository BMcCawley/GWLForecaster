"""
Custom exceptions used in GWLF.

Author:
    Brogan McCawley (16/08/2021)
"""


class Error(Exception):
    """Base class for other exceptions"""
    pass


class DirectoryNotEmptyError(Error):
    """Raised when a directory is not empty"""
    pass


class DiscontinuousTimeseriesError(Error):
    """Raised when a timeseries is not continuous i.e. has missing rows"""
    pass


class SeriesNotUniqueError(Error):
    """Raised when a series does not contain unique values."""
