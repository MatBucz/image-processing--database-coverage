"""Runs analysis for several databases provided in DB_SRC env var and stores results in OUTPUT dir"""
import logging
import os

from app.database_analyze import DatabaseAnalyze

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

DB_SRC = os.getenv("DB_SRC", "./example_dataset/")
OUTPUT = os.getenv("OUTPUT", "./output/")

if __name__ == "__main__":
    da = DatabaseAnalyze(DB_SRC, OUTPUT)
    da.analyze()
