#!/usr/bin/env python3
"""module for the function filter_datum"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """returns a log message obfuscated"""
    return re.sub(f'({"|".join(fields)})=[^;]*', f'\\1={redaction}', message)
