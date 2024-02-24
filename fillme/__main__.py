import os
import argparse
from sqlalchemy import create_engine
from fillme.core.FillMe import FillMe

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python module for FillMe!")

    # Add arguments
    parser.add_argument("--db-url", help="Database URL")
    parser.add_argument("--schema", help="Schema name")
    parser.add_argument("--openai-token", help="OpenAI API token")

    # Parse arguments
    args = parser.parse_args()

    # Check if arguments are provided
    if not args.db_url:
        parser.error("Please provide --db-url argument.")

    # set `OPENAI_API_KEY` if it is provided
    if args.openai_token:
        os.environ["OPENAI_API_KEY"] = args.openai_token

    # create SQLAlchemy engine
    sa_engine = create_engine(
        args.db_url,
        connect_args={'options': f"-csearch_path={args.db_url}"} if args.db_url else {},
    )

    # create FillMe and get started!
    fillme = FillMe(sa_engine)
    fillme.get_tables()
    fillme.generate_dummies()

