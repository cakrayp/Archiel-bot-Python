from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import os
load_dotenv()


# Current Path
current_path = os.getcwd()

# Variable Global
use_save_logs = True if os.getenv('SAVE_LOGS', 'False').lower() in ['true', 'True'] else False


# +---------[ Logger Folder ]---------+

logger_folder_path = Path(current_path, "discord_logs")
if not logger_folder_path.exists() and use_save_logs == True:
    # logger_folder_path.mkdir(parents=True, exist_ok=True)
    os.mkdir(logger_folder_path)


# +---------[ Logger Function ]---------+

# Created by 'CakraYP'
def loggerSetup(*message, **options):
    """
    Logs a message with a timestamp to a log file.

    Args:
        message (str): The message to log.
        Options:
            - `use_iso_date` (bool): Whether to use ISO date format in the log entry. Defaults to False.
            - `log_file (str)` The log file path. Defaults to "logger {ISO_DATE}.log".
    """
    iso_time = datetime.now().astimezone().isoformat(timespec='seconds')
    iso_date = datetime.now().astimezone().date().isoformat()

    # Default Logger Path if you does not use this paramenter.
    default_loggerPath = Path(current_path, "temp", f"logger {iso_date}.log")

    # Logger Path check
    isTypeStrOrPath = (isinstance(options.get('log_file', False), Path) or isinstance(options.get('log_file', False), str))
    
    # Path Custom as needed.
    log_file_path = options['log_file'] if ('log_file' in list(options.keys())) and isTypeStrOrPath else default_loggerPath
    log_entry = f"[{iso_time}]: {' '.join(message)}\n" if options.get('use_iso_date', False) == True else (" ".join(message) + "\n")

    try:
        print(log_entry.strip(), flush=True)
        if options.get('save_logger', False) == True:
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
    except Exception as e:
        print(f"Logging error: {e}")

# Example Usage
# loggerSetup("This is a log message.", use_iso_date=True, save_logger=True)

# +---------[ Export Logger Function ]---------+

def logger(*message):
    dateCurrent = datetime.now().astimezone().date().isoformat()
    log_file = Path(current_path, "discord_logs", f"logger {dateCurrent}.log")
    loggerSetup(
        *message,
        log_file=log_file,
        use_iso_date=True,
        save_logger=use_save_logs
    )