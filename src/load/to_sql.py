import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class SQLServerLoader:
    def __init__(self, engine):
        self.engine = engine

    def load(self, processed_files: dict):
        """
        Production-safe SQL Server loader
        Handles NaN, dtype conflicts, and ODBC bulk insert issues
        """

        for file_name, file_path in processed_files.items():

            table_name = self._table_name(file_name)

            df = pd.read_csv(file_path)

            # -----------------------------
            # 1. CLEAN COLUMN NAMES
            # -----------------------------
            df.columns = [c.strip().lower() for c in df.columns]

            # -----------------------------
            # 2. NORMALISE NULLS (CRITICAL FIX)
            # -----------------------------
            df = self._normalize_nulls(df)

            # -----------------------------
            # 3. SANITISE TYPES
            # -----------------------------
            df = self._sanitize_dtypes(df)

            # -----------------------------
            # 4. FINAL PYTHON-SAFE CONVERSION
            # -----------------------------
            df = df.astype(object).where(pd.notnull(df), None)

            # -----------------------------
            # 5. SAFE INSERT MODE (IMPORTANT FIX)
            # -----------------------------
            try:
                df.to_sql(
                    name=table_name,
                    con=self.engine,
                    if_exists="replace",
                    index=False,
                    chunksize=500,
                    method=None  # IMPORTANT: avoids ODBC bulk insert issues
                )

                logger.info(f"LOADED SUCCESSFULLY: {table_name}")

            except Exception as e:
                logger.error(f"FAILED LOADING {table_name}: {str(e)}")
                raise

    def _normalize_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardises all null representations
        """
        df = df.replace({np.nan: None, pd.NA: None})
        return df

    def _sanitize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fix SQL Server type incompatibilities
        """

        for col in df.columns:

            dtype = str(df[col].dtype)

            # UNSIGNED FIX (CRITICAL)
            if dtype in ("uint64", "uint32"):
                df[col] = df[col].astype("int64")

            # BOOLEAN FIX
            elif dtype == "bool":
                df[col] = df[col].astype("int64")

            # OBJECT CLEANUP (VERY IMPORTANT FOR STRINGS LIKE holiday_name)
            elif dtype == "object":
                df[col] = df[col].astype("string")

            # FLOAT SAFETY
            elif "float" in dtype:
                df[col] = df[col].astype("float64")

            # INT SAFETY
            elif "int" in dtype:
                df[col] = df[col].astype("int64")

        return df

    def _table_name(self, file_name: str):
        return file_name.replace(".csv", "").replace("-", "_").lower()