import logging
import os
import re


def setup_logger():
    log_format = ("%(asctime)s [%(filename)s:%(lineno)s - "
                  "%(funcName)20s() ] %(levelname)s: %(message)s")
    log_file_path = os.path.join(os.path.dirname(__file__), "debug.log")
    file_handler = logging.FileHandler(filename=log_file_path,
                                       mode='w',
                                       encoding='utf-8')
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(filter_sensitive_fields)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG if os.getenv('DEBUG') else logging.INFO)

    return logger


sensitive_fields = [
    '--api-key',
    'password',
]


def filter_sensitive_fields(record):
    if isinstance(record.args, dict):
        record.args = {
            k: ('****' if k in sensitive_fields else v)
            for k, v in record.args.items()
        }
    elif isinstance(record.args, tuple):
        record.args = tuple('****' if arg in sensitive_fields else arg
                            for arg in record.args)

    if isinstance(record.msg, str):
        record.msg = re.sub(r'\x1B\[?[\d;]*[mK]', '', record.msg)

    return True


logger = setup_logger()
