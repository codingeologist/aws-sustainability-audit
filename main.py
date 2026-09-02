"""Main CLI Module"""
import argparse
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


def main():
    """main loop"""

    parser = argparse.ArgumentParser(
        prog="AWS Sustainability Reporter",
        description="Download Sustainability Reports from an AWS Account"
    )

    parser.add_argument(
        "-a",
        "--add",
        help="add sustainability data from an authenticated AWS account to the local database"
    )
    parser.add_argument(
        "-e",
        "--export",
        type=str,
        help="export the database to a named file"
    )
    args = parser.parse_args()

    if args.export:
        export(filename=f"{args.export}.csv")
    elif args.add:
        add_data()


if __name__ == "__main__":

    main()
