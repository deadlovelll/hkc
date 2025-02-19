import os

import json
import logging
import socket
from logging import Logger, LogRecord, Formatter

import logstash


class CustomLogstashFormatter(Formatter):
    
    """
    Custom formatter for Logstash that outputs logs in JSON format encoded in UTF-8.
    """

    def format (
        self, 
        record: LogRecord,
    ) -> bytes:
        
        log_record = {
            "message": record.getMessage(),
            "level": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "host": socket.gethostname(),
            "method": record.funcName,
            "filename": record.filename,
            "line_number": record.lineno,
        }
        # Return JSON output as bytes
        return json.dumps(log_record).encode("utf-8")


class LoggerInitializer:
    
    """
    Initializes and configures a logger instance with a Logstash handler.
    """

    def __init__(
        self,
        logger_name: str = "fastapi-logger",
        logstash_host: str = os.getenv('LOGSTASH_HOST'),
        logstash_port: int = os.getenv('LOGSTASH_PORT'),
        level: int = logging.INFO,
    ) -> None:
        
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

        Returns:
            Logger: The configured logger.
        """
        
        logger: Logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.level)

        # Avoid adding multiple handlers if already configured
        if not logger.handlers:
            logstash_handler = logstash.LogstashHandler (
                host=self.logstash_host, 
                port=self.logstash_port, 
                version=1
            )
            logstash_handler.setFormatter(CustomLogstashFormatter())
            logger.addHandler(logstash_handler)

        return logger
