"""
main class for the FillMe package
"""

import os

import openai
from openai import OpenAI
from sqlalchemy import Engine, MetaData
from sqlalchemy.schema import CreateTable
from fillme.utils.exceptions import FillMeException

openai_api_key = os.environ.get('OPENAI_API_KEY')


class FillMe:

    def __init__(
            self,
            engine: Engine,
            tables_to_exclude=None,
            **kwargs
    ):
        """

        :param engine:
        :param tables_to_exclude:
        :param kwargs:
        """
        if tables_to_exclude is None:
            self.tables_to_exclude = []
        self.engine = engine
        self._check_engine()
        self.openai_model = kwargs.get(
            'openai_model',
            'gpt-3.5-turbo'
        )
        self.openai_client = self._openai_client()
        self.raw_sql = ''
        self.tables = []

    def _check_engine(self) -> None:
        """
        Checks if the engine is valid

        """

        try:
            self.engine.connect()
        except Exception as e:
            raise FillMeException(f'could not connect to database. message: {e}') from e

    def _openai_client(self) -> openai.Client:
        """
        initializes the OpenAI to use for dummy data
        generation

        :return: openai client instance
        """

        if openai_api_key is None:
            raise FillMeException('`OPENAI_API_KEY` is not in the OS environment variables')

        openai_client = OpenAI()

        # test connection with creating a completion task
        chat_completion = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say 'ok' lower case.",
                }
            ],
            model=self.openai_model,
        )

        if (len(chat_completion.choices) == 0 or
                'ok' not in chat_completion.choices[0].message.content.lower()):
            raise FillMeException('Failed connect to OpenAI API')
        return openai_client

    def get_tables(self) -> None:
        """
        gets all the tables in the database and removes
        excluded tables. then print out for check.

        """
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        self.raw_sql = ''
        self.tables = []
        for table in metadata.sorted_tables:
            if table.name not in self.tables_to_exclude:
                self.tables.append(table.name)
                self.raw_sql += CreateTable(table).compile(self.engine).__str__()
        print(f'detected tables from provided engine: {self.tables}')

    def generate_dummies(self) -> None:
        """
        generates dummy using openai instance and passing
        command containing tables and relationships

        """

        chat_completion = self.openai_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a SQL programmer, write SQL "
                               "to Fill tables with dummy values. plain SQL "
                               "statements with no explanation"
                },
                {
                    "role": "user",
                    "content": "create dummy data for this table: \n"+self.raw_sql
                }
            ],
            model="gpt-3.5-turbo",
        )
        if len(chat_completion.choices) == 0:
            raise FillMeException('OpenAI API Failed to generate dummy data')
        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                chat_completion.choices[0].message.content
            )
            cursor.close()
            connection.commit()
            connection.close()
        except Exception as e:
            raise FillMeException(f'Failed to put generated data into tables. message: {e}') from e
