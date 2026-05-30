import logging
import pandas as pd

logger = logging.getLogger(__name__)


class SQLReportWriter:
    def __init__(self, engine):
        self.engine = engine

    def save_report(self, report_df, run_id: str):
        """
        Writes data quality report to SQL Server.
        Accepts DataFrame or dict safely.
        """

        # -----------------------------
        # 1. NORMALISE INPUT TYPE
        # -----------------------------
        if isinstance(report_df, dict):
            report_df = pd.DataFrame(report_df)

        if report_df is None or report_df.empty:
            logger.warning("EMPTY DATA QUALITY REPORT - NOTHING WRITTEN TO SQL")
            return

        # -----------------------------
        # 2. ADD OBSERVABILITY COLUMN
        # -----------------------------
        report_df = report_df.copy()
        report_df["run_id"] = run_id

        # -----------------------------
        # 3. ENSURE SQL SAFE TYPES
        # -----------------------------
        report_df = report_df.where(pd.notnull(report_df), None)

        # -----------------------------
        # 4. WRITE TO SQL SERVER
        # -----------------------------
        try:
            report_df.to_sql(
                name="data_quality_report",
                con=self.engine,
                if_exists="append",
                index=False,
                chunksize=500,
                method=None   # IMPORTANT: avoids SQL Server bulk insert issues
            )

            logger.info(f"DATA QUALITY REPORT WRITTEN | RUN_ID: {run_id}")

        except Exception as e:
            logger.error(f"FAILED TO WRITE DATA QUALITY REPORT | ERROR: {str(e)}")
            raise