from app.database_metrics import DatabaseMetrics

if __name__ == "__main__":
    DB_SRC = "/app/example_dataset/"
    OUTPUT = "/app/output/"

    db = DatabaseMetrics(DB_SRC, OUTPUT)
    db.calculate_si_cf()
    db.si_cf_plane()
