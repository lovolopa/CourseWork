import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

import pandas as pd


def logger_setup() -> Logger:
    """Logger для опредления правельности функций"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logger.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


logger = logger_setup()


def read_xlsx(filename: Any) -> Any | Path:
    """Функция читает файл XLSX или JSON файл"""
    if Path(filename).suffix.lower() == ".xlsx":
        read = pd.read_excel(filename)
        return read.to_dict(orient="records")
    else:
        raise ValueError("Invalid file format")


def write_data(file_format: str, result: Any) -> None:
    """Функция выписывает результат в специальный файл"""
    if file_format.endswith(".txt"):
        with open(file_format, "a", encoding="utf-8") as file:
            file.write(result)
    else:
        with open(file_format, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
