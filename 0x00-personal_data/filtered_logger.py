#!/usr/bin/env python3
"""contains a function that obfuscates log message"""
import logging
from typing import List
import re
import mysql.connector
import os

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """contains a function that obfuscates log message"""
    for i in fields:
        message = re.sub(f'{i}=.*?{separator}',
                         f'{i}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter vaues in incoming log record"""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """creates and returns new logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects to database"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        user=username, password=password, host=host, database=db)
    return conn


def main():
    """logs users data from db"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    for (name, email, phone, ssn, password, ip, last_login,
         user_agent) in cursor:
        logger.info(
            f'name={name}; email={email}; phone={phone}; ssn={ssn}; \
password={password}; ip={ip}; last_login={last_login}; \
user_agent={user_agent};')
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
