# ytmusic_importer/utils.py

import json
import os
import time
from typing import Any, Callable

def log(msg: str):
    print(f"[ytmusic-import] {msg}")


def log_error(msg: str):
    print(f"[ytmusic-import][ERROR] {msg}")


def retry(
    func: Callable,
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Any:
    """
    Retry a function with exponential backoff.
    """
    attempt = 0

    while attempt < retries:
        try:
            return func()
        except exceptions as e:
            attempt += 1

            if attempt >= retries:
                raise

            sleep_time = delay * (backoff ** (attempt - 1))
            log_error(f"Retry {attempt}/{retries} failed: {e}")
            time.sleep(sleep_time)


def save_checkpoint(path: str, data: dict):
    with open(path, "w") as f:
        json.dump(data, f)


def load_checkpoint(path: str) -> dict:
    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)


def ensure_file_exists(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")


def ensure_columns(df, required_columns):
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def rate_limit_sleep(delay: float):
    if delay > 0:
        time.sleep(delay)