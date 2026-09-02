"""utility helper module"""
import json
from datetime import datetime
from sustainability.database import Database


class DateTimeEncoder(json.JSONEncoder):
    """datetime encoder for json exports"""
    def default(self, obj):
        """datetime obj to str"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def export_data(db_path: str, table_name: str, filename: str) -> None:
    """
    export data to file
    """

    db = Database(db_path=db_path)
    df = db.read_table(name=table_name)
    df.to_csv(filename, index=False)
