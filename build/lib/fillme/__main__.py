import argparse
from fillme.core.FillMe import FillMe
from sqlalchemy import create_engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python module for FillMe!")

    # Add arguments
    parser.add_argument("db-url", help="Database URL")
    parser.add_argument("schema", help="Schema name")

    # Parse arguments
    args = parser.parse_args()

    sa_engine = create_engine(
        args.db_url,
        connect_args={'options': f"-csearch_path={args.db_url}"} if args.db_url else {},
    )

    fillme = FillMe(sa_engine)
    fillme.get_tables().generate_dummies()

