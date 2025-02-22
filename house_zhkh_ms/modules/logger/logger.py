import os

import json
import logging
import socket
from logging import Logger, LogRecord, Formatter

import logstash


class CustomLogstashFormatter(Formatter):
    
    """
    Custom formatter for Logstash that outputs logs in JSON format encoded in UTF-8.

    This formatter customizes the output of log records to match the expected format for Logstash.
    It outputs logs as JSON, which includes important fields such as message, log level, timestamp,
    host, method name, filename, and line number.
    """

    def format (
        self, 
        record: LogRecord,
    ) -> bytes:
        
        """
        Formats the log record into a JSON-encoded byte string.

        Args:
            record (LogRecord): The log record to be formatted.

        Returns:
            bytes: The JSON-formatted log record as a byte string.
        """
        
        log_record = {
            "message": record.getMessage(),
            "level": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "host": socket.gethostname(),
            "method": record.funcName,
            "filename": record.filename,
            "line_number": record.lineno,
        }
        return json.dumps(log_record).encode("utf-8")


class LoggerInitializer:
    
    """
    Initializes and configures a logger instance with a Logstash handler.

    This class is responsible for setting up a logger with a Logstash handler that sends log
    entries to a remote Logstash server in JSON format. It also allows for the configuration of
    logging level, Logstash host, and port.
    """

    def __init__(
        self,
        logger_name: str = "fastapi-logger",
        logstash_host: str = os.getenv('LOGSTASH_HOST'),
        logstash_port: int = os.getenv('LOGSTASH_PORT'),
        level: int = logging.INFO,
    ) -> None:
        
        """
        Initializes the LoggerInitializer with configuration parameters.

        Args:
            logger_name (str): The name of the logger. Defaults to 'fastapi-logger'.
            logstash_host (str): The Logstash server host. Defaults to the environment variable 'LOGSTASH_HOST'.
            logstash_port (int): The Logstash server port. Defaults to the environment variable 'LOGSTASH_PORT'.
            level (int): The logging level. Defaults to logging.INFO.
        """
        
        self.logger_name = logger_name
        self.logstash_host = logstash_host
        self.logstash_port = logstash_port
        self.level = level

    def init_logger (
        self,
    ) -> Logger:
        
        """
        Configures the logger with a Logstash handler and custom formatter,
        then returns the logger instance.

        The logger is configured to send logs to the specified Logstash server in JSON format,
        with relevant fields for tracking.

        Returns:
            Logger: The configured logger.
        """
        
        logger: Logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.level)

        if not logger.handlers:
            logstash_handler = logstash.LogstashHandler(
                host=self.logstash_host, 
                port=self.logstash_port, 
                version=1
            )
            logstash_handler.setFormatter(CustomLogstashFormatter())
            logger.addHandler(logstash_handler)

        return logger