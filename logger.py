from datetime import datetime
from pathlib import Path
import os


# Current Path
current_path = os.getcwd()


# +---------[ Logger Classes ]---------+

# Created by 'CakraYP'
class LoggerSetup:
    """
    LoggerSetup provides a simple timestamped logger.

    Usage:
        logger = LoggerSetup(log_file="app.log", use_iso_date=True, save_logger=True)
        logger.logger("This is a log message")

    Args:
        log_file (str, optional): Path to log file. If omitted, defaults to
            history-logs/logger YYYY-MM-DD.log in the current working directory.
        use_iso_date (bool): Whether to include an ISO timestamp with each entry.
        save_logger (bool): If True, log entries are also appended to disk.
    """

    def __init__(self, log_file=None, use_iso_date=True, save_logger=False):
        __logger_folder_path = Path(current_path, "history-logs")
        if (save_logger and log_file==None) and (not __logger_folder_path.exists()):
            os.makedirs(__logger_folder_path, exist_ok=True)

        __date_current = datetime.now().astimezone().date().isoformat()
        __default_log_file = Path(__logger_folder_path, f"logger {__date_current}.log")
        self.__log_file = Path(log_file) if log_file else __default_log_file
        self.__use_iso_date = use_iso_date
        self.__save_logger = save_logger
        

    def logger(self, *message):
        """
        Logs a message with a timestamp to a log file.

        Args:
            message (str): The message to log.
        """
        options = {}
        options['log_file'] = self.__log_file
        options['use_iso_date'] = self.__use_iso_date
        options['save_logger'] = self.__save_logger

        iso_time = datetime.now().astimezone().isoformat(timespec='seconds')
        log_file_path = options['log_file']
        log_entry = f"[{iso_time}]: {' '.join(message)}\n" if options.get('use_iso_date', False) == True else (" ".join(message) + "\n")

        # Main
        try:
            print(log_entry.strip(), flush=True)
            if options.get('save_logger', False) == True:
                with open(log_file_path, "a", encoding="utf-8") as f:
                    f.write(log_entry)
        except Exception as e:
            print(f"Logging error: {e}")
            print(e)
