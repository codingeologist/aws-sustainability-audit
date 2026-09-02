"""Main CLI Module"""
from sustainability.reports import Emissions
from sustainability.utils import export_data


def add_data():
    """add sustainability data from AWS SDK"""

    emissions = Emissions()
    carbon_data = emissions.get_carbon(start_year=2023, end_year=2027)
    emissions.data_transform(data=carbon_data)


def export(filename: str):
    """export data"""

    export_data(
        db_path="aws_carbon_emissions.db",
        table_name="emissions",
        filename=filename
    )


if __name__ == "__main__":

    add_data()
