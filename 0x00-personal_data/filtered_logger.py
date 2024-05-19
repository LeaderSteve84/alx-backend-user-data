#!/usr/bin/env python3
"""module for the function filter_datum"""
from typing import List
import re


def filter_datum(fields:[str], redaction: str, message: str, separator: str) -> str:
    """filter's a log lines.
    Args:
        fields (list[str]): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field will be obfuscated
        message (str): a string representing the log line
        separator (str):  a string representing by which character is
        separating all fields in the log line (message)
        Return: the log message obfuscated
    """


