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
from mysql import connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    ''' returns log data perosnal data (fields) obfuscated '''
    for fld in fields:
        message = re.sub(fld + '=.*?' + separator,
                         fld + '=' + redaction+separator, message)
    return message


def get_db() -> connector:
    ''' returns a connector to the database '''
    uname = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME', '')
    con = connector.connect(
                            host=host,
                            database=db,
                            user=uname,
                            password=passwd)
    return con


def main():
    ''' displays the log data from db  '''
    connection = get_db()
    query = 'SELECT * FROM users'
    cursor = connection.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    for line in result:
        line_lst = []
        pii = ['name', 'email', 'phone', 'ssn', 'password']
        line_lst.append('name=' + line[0])
        line_lst.append('email=' + line[1])
        line_lst.append('phone=' + line[2])
        line_lst.append('ssn=' + line[3])
        line_lst.append('password=' + line[4])
        line_lst.append('ip=' + line[5])
        line_lst.append('last_login=' + str(line[6]))
        line_lst.append('user_agent=' + line[7])
        line_str = ';'.join(str(fld) for fld in line_lst)
        logger = get_logger()
        filtered = filter_datum(pii, '***', line_str + ';', ';')
        logger.info(filtered)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialize class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ return formated and filtered log """
        formatted = super(RedactingFormatter, self).format(record)
        filtered = filter_datum(self.fields, self.REDACTION, formatted,
                                self.SEPARATOR)
        return filtered


def get_logger() -> logging.Logger:
    ''' return logging logger '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


if __name__ == '__main__':
    main()
