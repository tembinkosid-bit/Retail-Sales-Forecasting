import logging
import uuid
import pandas as pd

logger = logging.getLogger(__name__)


class DataPipeline:
    def __init__(self, extractor, validator, transformer, loader, report_writer=None):
        self.extractor = extractor
        self.validator = validator
        self.transformer = transformer
        self.loader = loader
        self.report_writer = report_writer

    def run(self, dataset: str):
        run_id = str(uuid.uuid4())

        try:
            logger.info(f"PIPELINE STARTED | RUN_ID: {run_id}")

            # -----------------------
            # 1. EXTRACT
            # -----------------------
            logger.info("STAGE 1: EXTRACTION STARTED")
            extracted_path = self.extractor.download_dataset(dataset)
            logger.info(f"STAGE 1 COMPLETE: {extracted_path}")

            # -----------------------
            # 2. VALIDATE
            # -----------------------
            logger.info("STAGE 2: VALIDATION STARTED")

            validation_result = self.validator.validate_directory(extracted_path)

            validated_data = validation_result["data"]
            report_df = validation_result["report_df"]

            logger.info("STAGE 2 COMPLETE")

            # -----------------------
            # 3. TRANSFORM
            # -----------------------
            logger.info("STAGE 3: TRANSFORMATION STARTED")
            processed_files = self.transformer.transform(validated_data)
            logger.info("STAGE 3 COMPLETE")

            # -----------------------
            # 4. OBSERVABILITY LAYER (SQL REPORT)
            # -----------------------
            if self.report_writer:

                # HARD GUARANTEE: always DataFrame
                if not isinstance(report_df, pd.DataFrame):
                    report_df = pd.DataFrame(report_df)

                # safety: ensure schema consistency
                if report_df.empty:
                    logger.warning("DATA QUALITY REPORT IS EMPTY (writing schema-only record)")

                logger.info("SAVING DATA QUALITY REPORT TO SQL SERVER")

                self.report_writer.save_report(
                    report_df=report_df,
                    run_id=run_id
                )

            # -----------------------
            # 5. LOAD (SQL SERVER)
            # -----------------------
            logger.info("STAGE 4: LOADING STARTED")
            self.loader.load(processed_files)
            logger.info("STAGE 4 COMPLETE")

            logger.info(f"PIPELINE SUCCESSFULLY COMPLETED | RUN_ID: {run_id}")

            return {
                "status": "success",
                "run_id": run_id,
                "extracted_path": extracted_path,
                "processed_files": processed_files
            }

        except Exception as e:
            logger.error(f"PIPELINE FAILED | RUN_ID: {run_id} | ERROR: {str(e)}")
            raise