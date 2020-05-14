import os

from app.database_metrics import DatabaseMetrics

if __name__ == "__main__":
    DB_SRC = "/app/example_dataset/"
    OUTPUT = "/app/output/"

    for db in next(os.walk(DB_SRC))[1]:
        db_metric = DatabaseMetrics(DB_SRC + db, OUTPUT, db)
        db_metric.plot_all()