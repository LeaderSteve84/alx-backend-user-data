#!/usr/bin/env python3
"""module for the function filter_datum"""
from typing import List
import re
import logging


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """returns a log message obfuscated"""
    return re.sub(f'({"|".join(fields)})=[^;]*', f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return super().format(record).replace(record.getMessage(),
filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR))
