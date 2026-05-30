import logging

from src.extract.kaggle_extractor import KaggleExtractor
from src.validate.validation import DataValidator
from src.transform.cleaning import DataTransformer
from src.load.to_sql import SQLServerLoader
from src.pipeline.pipeline import DataPipeline

from urllib.parse import quote_plus
from sqlalchemy import create_engine


# -----------------------------
# LOGGING CONFIG
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------
# SQL SERVER ENGINE
# -----------------------------
def get_sql_engine():
    connection_string = quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MBETHIE-PC\\SQLEXPRESS;"
        "DATABASE=retail_db;"
        "Trusted_Connection=yes;"
    )

    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={connection_string}"
    )


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():

    logger.info("INITIALIZING ETL PIPELINE")

    # -----------------------------
    # COMPONENTS
    # -----------------------------
    extractor = KaggleExtractor(raw_data_dir="data/raw")

    validator = DataValidator()

    transformer = DataTransformer(processed_data_dir="data/processed")

    # IMPORTANT FIX: engine is created here, injected into loader
    sql_engine = get_sql_engine()
    loader = SQLServerLoader(engine=sql_engine)

    # -----------------------------
    # PIPELINE ORCHESTRATION
    # -----------------------------
    pipeline = DataPipeline(
        extractor=extractor,
        validator=validator,
        transformer=transformer,
        loader=loader
    )

    dataset = "noopurbhatt/retail-store-sales-forecasting-dataset"

    result = pipeline.run(dataset)

    logger.info("PIPELINE COMPLETED SUCCESSFULLY")

    print("\n================ PIPELINE RESULT ================")
    print(result)
    print("=================================================\n")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()