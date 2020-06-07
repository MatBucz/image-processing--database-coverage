"""Runs analysis for several databases provided in DB_SRC env var and stores results in OUTPUT dir"""
import logging
import os

from app.database_analyze import DatabaseAnalyze

LOGGING_LEVEL = int(os.getenv("LOGGING_LEVEL", logging.WARNING))

logging.basicConfig(level=LOGGING_LEVEL)

DB_SRC = os.getenv("DB_SRC", "./example_dataset/")
OUTPUT = os.getenv("OUTPUT", "./output/")

if __name__ == "__main__":
    da = DatabaseAnalyze(DB_SRC, OUTPUT)
    da.analyze()
