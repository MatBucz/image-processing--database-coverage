"""Runs analysis for several databases provided in DB_SRC env var and stores results in OUTPUT dir"""
import math
import os
from typing import List

from app.database_metrics import DatabaseMetrics, DatabaseMetricsError

DB_SRC = os.getenv("DB_SRC", "./example_dataset/")
OUTPUT = os.getenv("OUTPUT", "./output/")

MAX_SI = float(os.getenv("MAX_SI", 162.22798137900915))
MAX_CF = float(os.getenv("MAX_CF", 140.38326742526147))

max_si_list: List[float] = []
max_cf_list: List[float] = []

if __name__ == "__main__":

    if not os.path.isdir(DB_SRC):
        raise ValueError(f"Given path '{DB_SRC}' is not valid directory")
    for db in next(os.walk(DB_SRC))[1]:
        db_metric = DatabaseMetrics(DB_SRC + db, OUTPUT, (MAX_SI, MAX_CF), db)
        si, cf = db_metric.get_max_si_cf()
        max_si_list.append(si)
        max_cf_list.append(cf)
        db_metric.plot_all()

    max_si = max(max_si_list)
    max_cf = max(max_cf_list)
    if not math.isclose(MAX_SI, max_si, rel_tol=1e-03) or not math.isclose(
        MAX_CF, max_cf, rel_tol=1e-03
    ):
        raise DatabaseMetricsError(
            f"Make sure your env MAX_SI and MAX_CF values are set according to the:\n"
            f"Max SI value: {max_si}, Max CF value: {max_cf}\n"
            f"Provided SI:  {MAX_SI}, provided CF:  {MAX_CF}"
        )
