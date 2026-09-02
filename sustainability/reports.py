"""Report Module"""
from datetime import datetime
import boto3
import pandas as pd
from sustainability.database import Database


class Emissions:
    """emissions report class"""

    def __init__(self) -> None:

        self.db_name = "aws_carbon_emissions.db"
        self.client = boto3.client("sustainability", region_name="us-east-1")
        self.account_id = ""
        self.account_name = ""


    def get_account(self) -> None:
        """get aws account id"""

        self.account_id = boto3.client("sts").get_caller_identity().get("Account")

    def get_carbon(self, start_year: int, end_year: int):
        """get carbon emissions report"""

        response = self.client.get_estimated_carbon_emissions(
            TimePeriod={
                "Start": datetime(start_year, 1, 1),
                "End": datetime(end_year, 1, 1)
            },
            GroupBy=["REGION"],
            EmissionsTypes=["TOTAL_LBM_CARBON_EMISSIONS", "TOTAL_MBM_CARBON_EMISSIONS"],
            Granularity="MONTHLY"
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return response["Results"]
        else:
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            raise ConnectionError(
                f"Unable to retrieve carbon emission estimates with status code: {status_code}")


    def data_transform(self, data: dict):
        """transform data"""

        self.get_account()
        cols = {
            "ModelVersion": "model",
            "TimePeriod.Start": "start_date",
            "TimePeriod.End": "end_date",
            "DimensionsValues.REGION": "region",
            "EmissionsValues.TOTAL_LBM_CARBON_EMISSIONS.Value": "total_lbm_emissions",
            "EmissionsValues.TOTAL_MBM_CARBON_EMISSIONS.Value": "total_mbm_emissions",
            "EmissionsValues.TOTAL_MBM_CARBON_EMISSIONS.Unit": "unit"
        }

        df = pd.json_normalize(data)
        df.insert(loc=0, column="account_id", value=self.account_id)
        df.drop(df.columns[6], axis=1, inplace=True)
        df.rename(columns=cols, inplace=True)

        db = Database(db_path=self.db_name)
        db.create_table(name="emissions", df=df)
        print("Data Written to DB")
