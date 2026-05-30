import os
import logging
import pandas as pd

from src.utils.data_quality_report import DataQualityReport

logger = logging.getLogger(__name__)


class DataValidator:
    def __init__(self, expected_columns: list = None):
        self.expected_columns = expected_columns
        self.report = None  # will be reset per run

    def validate_directory(self, extracted_path: str) -> dict:
        try:
            logger.info(f"VALIDATION STARTED FOR DIRECTORY: {extracted_path}")

            # ---------------------------------
            # RESET REPORT PER RUN (IMPORTANT FIX)
            # ---------------------------------
            self.report = DataQualityReport()

            files = self._get_data_files(extracted_path)

            if not files:
                raise FileNotFoundError("No data files found in extracted folder")

            validated_data = {}

            for file_path in files:
                logger.info(f"VALIDATING FILE: {file_path}")

                df = self._load_file(file_path)

                self._validate_structure(df, file_path)
                self._validate_quality(df, file_path)

                file_name = os.path.basename(file_path)

                # STORE METRICS
                self.report.add_file_stats(file_name, df)

                validated_data[file_name] = df

            # ---------------------------------
            # SAFETY CHECK (CRITICAL FIX)
            # ---------------------------------
            report_df = self.report.to_dataframe()

            if report_df.empty:
                logger.warning("DATA QUALITY REPORT IS EMPTY AFTER VALIDATION")

            logger.info("VALIDATION COMPLETED SUCCESSFULLY")

            return {
                "data": validated_data,
                "report_df": report_df
            }

        except Exception as e:
            logger.error(f"VALIDATION FAILED: {str(e)}")
            raise

    def _get_data_files(self, folder: str):
        supported_extensions = (".csv", ".json", ".xlsx")

        file_paths = []
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(supported_extensions):
                    file_paths.append(os.path.join(root, file))

        return file_paths

    def _load_file(self, file_path: str) -> pd.DataFrame:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            return pd.read_json(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    def _validate_structure(self, df: pd.DataFrame, file_path: str):
        logger.info(f"STRUCTURE CHECK: {file_path}")

        if df.empty:
            raise ValueError(f"Empty dataset: {file_path}")

        if self.expected_columns:
            missing = set(self.expected_columns) - set(df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {missing}")

    def _validate_quality(self, df: pd.DataFrame, file_path: str):
        logger.info(f"QUALITY CHECK: {file_path}")

        null_ratio = df.isnull().mean()
        bad_null_cols = null_ratio[null_ratio > 0.5].index.tolist()

        if bad_null_cols:
            logger.warning(f"High null ratio: {bad_null_cols}")

        dup_ratio = df.duplicated().mean()

        if dup_ratio > 0.2:
            logger.warning(f"High duplicates: {dup_ratio:.2%}")