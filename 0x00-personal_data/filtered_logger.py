#!/usr/bin/env python3
''' Write a function called filter_datum that returns the
log message obfuscated:

Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character is separating all
fields in the log line (message)
The function should use a regex to replace occurrences of certain
field values.
filter_datum should be less than 5 lines long and use re.sub to
perform the substitution with a single regex.
 '''
import re
import os
import logging
import mysql.connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(field: List[str], redaction: str, message: str,
                 separator: str) -> str:
    ''' returns log data perosnal data (fields) obfuscated '''
    for f in field:
        pt_pass = r'\b{}=[\s\S]*?(?={})\b{}'.format(f, separator, separator)
        replace_pass = '{}={}{}'.format(f, redaction, separator)
        message = re.sub(pt_pass, replace_pass, message)
    return message


def get_logger() -> logging.Logger:
    ''' return logging logger '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagete = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector:
    ''' returns a connector to the database '''
    uname = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME', '')
    connection = mysql.connector.connect(host=host,
                                         database=db,
                                         user=uname,
                                         password=passwd)
    if connection.is_connected():
        return connection
    return None


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        ''' initialize class '''
        self.FIELDS = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        ''' return formated and filtered log '''
        formatted = super(RedactingFormatter, self).format(record)
        filtered = filter_datum(self.FIELDS, self.REDACTION, formatted,
                                self.SEPARATOR)
        return filtered
