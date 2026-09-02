"""Database Module"""
import duckdb
import pandas as pd


class Database:
    """Database Connection"""

    def __init__(self, db_path: str = ":memory:") -> None:

        self.path = db_path
        self.conn = duckdb.connect(database=self.path, read_only=False)


    def create_table(self, name: str, df: pd.DataFrame):
        """create emissions table"""

        self.conn.register(f"{name}_df", df)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS emissions (
                account_id TEXT,
                model TEXT,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                region TEXT,
                total_lbm_emissions DOUBLE,
                total_mbm_emissions DOUBLE,
                unit TEXT
            )
            """
        )
        self.conn.execute(f"INSERT into {name} SELECT * FROM {name}_df")


    def read_table(self, name: str) -> pd.DataFrame:
        """read a specified table name"""

        query = f"SELECT * FROM {name}"
        return self.conn.execute(query).fetchdf()
