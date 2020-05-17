"""Runs analysis for several databases provided in DB_SRC env var and stores results in OUTPUT dir"""
import os

from app.database_metrics import DatabaseMetrics

if __name__ == "__main__":
    DB_SRC = os.getenv("DB_SRC", "./example_dataset/")
    OUTPUT = os.getenv("OUTPUT", "./output/")

    if not os.path.isdir(DB_SRC):
        raise ValueError(f"Given path '{DB_SRC}' is not valid directory")
    for db in next(os.walk(DB_SRC))[1]:
        db_metric = DatabaseMetrics(DB_SRC + db, OUTPUT, db)
        db_metric.plot_all()
