import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self, processed_data_dir: str):
        self.processed_data_dir = processed_data_dir
        os.makedirs(self.processed_data_dir, exist_ok=True)

    def transform(self, validated_data: dict) -> dict:
        """
        Accepts multiple validated DataFrames and processes each independently
        Returns dictionary of processed file paths
        """
        try:
            logger.info("TRANSFORMATION STARTED (MULTI-DATASET MODE)")

            processed_outputs = {}

            for file_name, df in validated_data.items():
                logger.info(f"TRANSFORMING: {file_name}")

                cleaned_df = self._clean_data(df)
                engineered_df = self._engineer_features(cleaned_df)

                output_path = self._save_data(engineered_df, file_name)

                processed_outputs[file_name] = output_path

                logger.info(f"COMPLETED: {file_name} → {output_path}")

            logger.info("ALL TRANSFORMATIONS COMPLETE")

            return processed_outputs

        except Exception as e:
            logger.error(f"TRANSFORMATION FAILED: {str(e)}")
            raise

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standard cleaning logic applied per dataset
        """
        logger.info("CLEANING DATA")

        df = df.copy()

        # normalize columns
        df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df.columns
        ]

        # remove duplicates
        df = df.drop_duplicates()

        # remove fully empty rows
        df = df.dropna(how="all")

        return df

    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Feature engineering placeholder (dataset-agnostic)
        """
        logger.info("ENGINEERING FEATURES")

        # Safe generic feature example
        df["row_hash"] = pd.util.hash_pandas_object(df, index=False)

        return df

    def _save_data(self, df: pd.DataFrame, file_name: str) -> str:
        """
        Save each transformed dataset separately
        """
        base_name = os.path.splitext(file_name)[0]

        output_path = os.path.join(
            self.processed_data_dir,
            f"{base_name}_processed.csv"
        )

        df.to_csv(output_path, index=False)

        logger.info(f"SAVED: {output_path}")

        return output_path