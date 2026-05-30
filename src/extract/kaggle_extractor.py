import os
import logging
import zipfile
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi

logger = logging.getLogger(__name__)


class KaggleExtractor:
    def __init__(self, raw_data_dir: str):
        self.raw_data_dir = raw_data_dir
        os.makedirs(self.raw_data_dir, exist_ok=True)

        self.api = KaggleApi()
        self.api.authenticate()

    def download_dataset(self, dataset: str) -> str:
        """
        Downloads Kaggle dataset and extracts it into raw folder
        """
        try:
            logger.info(f"STARTING DATASET DOWNLOAD: {dataset}")

            # Download dataset as ZIP
            self.api.dataset_download_files(
                dataset,
                path=self.raw_data_dir,
                unzip=False
            )

            zip_file = self._find_latest_zip()

            if not zip_file:
                raise FileNotFoundError("No ZIP file found after download")

            extract_path = self._extract_zip(zip_file)

            logger.info(f"DATASET READY AT: {extract_path}")

            return extract_path

        except Exception as e:
            logger.error(f"Kaggle ingestion failed: {str(e)}")
            raise

    def _find_latest_zip(self):
        """
        Find latest downloaded ZIP in raw folder
        """
        zips = [
            f for f in os.listdir(self.raw_data_dir)
            if f.endswith(".zip")
        ]

        if not zips:
            return None

        zips.sort(key=lambda x: os.path.getmtime(
            os.path.join(self.raw_data_dir, x)
        ))

        return os.path.join(self.raw_data_dir, zips[-1])

    def _extract_zip(self, zip_path: str) -> str:
        """
        Extract ZIP into structured folder
        """
        folder_name = os.path.basename(zip_path).replace(".zip", "")
        extract_folder = os.path.join(self.raw_data_dir, folder_name)

        os.makedirs(extract_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        logger.info(f"EXTRACTED TO: {extract_folder}")

        return extract_folder