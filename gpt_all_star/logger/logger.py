import logging
import os
import re

sensitive_fields = [
    "--api-key",
    "password",
]


def mask_sensitive_fields(record):
    if isinstance(record.args, dict):
        record.args = {
            k: ("****" if k in sensitive_fields else v) for k, v in record.args.items()
        }
    elif isinstance(record.args, tuple):
        record.args = tuple(
            "****" if arg in sensitive_fields else arg for arg in record.args
        )

    if isinstance(record.msg, str):
        record.msg = re.sub(r"\x1B\[?[\d;]*[mK]", "", record.msg)

    return True


class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        return mask_sensitive_fields(record)


def setup_logger():
    log_format = (
        "%(asctime)s [%(filename)s:%(lineno)s - "
        "%(funcName)20s() ] %(levelname)s: %(message)s"
    )
    log_file_name = os.path.join(os.path.dirname(__file__), "debug.log")
    file_handler = logging.FileHandler(
        filename=log_file_name, mode="w", encoding="utf-8"
    )
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(SensitiveDataFilter())

    _logger = logging.getLogger()
    _logger.addHandler(file_handler)
    _logger.setLevel(logging.DEBUG if os.getenv("DEBUG") else logging.INFO)

    return _logger


logger = setup_logger()
