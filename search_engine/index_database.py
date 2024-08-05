from whoosh.fields import Schema, TEXT, NGRAM
from whoosh.index import create_in, Index
from pymongo import MongoClient
import os
from typing import Any


class DatabaseIndex:
    """
    A class to create and manage an index for a MongoDB collection using Whoosh.

    Attributes:
        index_dir (str): The directory where the index will be stored.
        database (str): The name of the MongoDB database.
        db_connection_address (str): The MongoDB connection string.
    """

    def __init__(self, index_dir: str, database: str, db_connection_address: str = 'mongodb://localhost:27017'):
        self.index_dir = index_dir
        self.database = database
        self.db_connection_address = db_connection_address

        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

    @staticmethod
    def get_schema() -> Schema:
        """
        Returns the schema used for indexing the documents.

        Returns:
            Schema: The Whoosh schema for indexing.
        """
        return Schema(
            numer_ksiegi=NGRAM(stored=True, minsize=3, maxsize=5),
            typ_ksiegi=NGRAM(stored=True, minsize=3, maxsize=5),
            oznaczenie_wydzialu=NGRAM(stored=True, minsize=3, maxsize=5),
            data_zapisania=TEXT(stored=True),
            polozanie=NGRAM(stored=True, minsize=3, maxsize=5),
            wlasciciel=NGRAM(stored=True, minsize=3, maxsize=5),
            dzial_i_o=TEXT(stored=True),
            dzial_i_sp=TEXT(stored=True),
            dzial_ii=TEXT(stored=True),
            dzial_iii=TEXT(stored=True),
            dzial_iv=TEXT(stored=True)
        )

    def connect_to_db(self) -> Any:
        """
        Connects to the MongoDB database and returns the collection.

        Returns:
            Collection: The MongoDB collection object.
        """
        mongo_client = MongoClient(self.db_connection_address)
        mongo_db = mongo_client[self.database]
        return mongo_db['data']

    def create_index(self) -> None:
        """
        Creates an index from the MongoDB data collection using the defined schema.
        """
        ix: Index = create_in(self.index_dir, self.get_schema())
        writer = ix.writer()
        records = self.connect_to_db().find()

        for record in records:
            writer.add_document(
                numer_ksiegi=record.get("Numer księgi wieczystej", ""),
                typ_ksiegi=record.get("Typ księgi wieczystej", ""),
                oznaczenie_wydzialu=record.get("Oznaczenie wydziału prowadzącego księgę wieczystą", ""),
                data_zapisania=record.get("Data zapisania księgi wieczystej", ""),
                polozanie=record.get("Położenie", ""),
                wlasciciel=record.get("Właściciel / użytkownik wieczysty / uprawniony", ""),
                dzial_i_o=record.get("Dział I-O", ""),
                dzial_i_sp=record.get("Dział I-Sp", ""),
                dzial_ii=record.get("Dział II", ""),
                dzial_iii=record.get("Dział III", ""),
                dzial_iv=record.get("Dział IV", "")
            )

        writer.commit()


if __name__ == "__main__":
    indexer = DatabaseIndex('indexdir', 'evidence_books_metadata')
    indexer.create_index()
