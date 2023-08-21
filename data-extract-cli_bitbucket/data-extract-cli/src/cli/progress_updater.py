from __future__ import annotations
from abc import ABC, abstractmethod
import logging

"""
Provides a framework to keep the CLI seperate from our implementation classes.
Any progress updaters need to implement this abstract class.
The purpose is to receive "external" updates on the extract Process.
For example loading bars or appending to CSV files
"""


class ProgressUpdater(ABC):

    @abstractmethod
    def update(self, message: str = None, data: dict = None) -> ProgressUpdater:
        raise Exception(
            "A Progress Updater needs to implement the `update` method")

    @abstractmethod
    def success(self, message: str) -> ProgressUpdater:
        raise Exception(
            "A Progress Updater needs to implement the `success` method")

    @abstractmethod
    def error(self, error: str) -> ProgressUpdater:
        raise Exception(
            "A Progress Updater needs to implement the `error` method")

    @abstractmethod
    def set_length(self, length: int) -> ProgressUpdater:
        logging.warning(
            'Trying to set length on Progress Updater but the implementation is empty.')
