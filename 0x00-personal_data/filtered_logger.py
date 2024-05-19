#!/usr/bin/env python3
"""module for the function filter_datum"""
import os
import mysql.connector
from typing import List
import re
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        """format method"""
        return super().format(record).replace(record.getMessage(), filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
        ))


def get_logger() -> logging.Logger:
    """Returns a loggings.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    try:
        connection = mysql.connector.connection.MySQLConnection(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def main():
    """The function will obtain a database connection using get_db
     and retrieve all rows in the users table and display
     each row under a filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    descript = [descpt[0] for descpt in cursor.description]

    logger = get_logger()

    for user in cursor:
        user_info = "".join(
                f'{des}={str(usr)}; ' for usr, des in zip(user, descript)
            )
        logger.info(user_info)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
