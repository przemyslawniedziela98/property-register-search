from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.query import Query
from whoosh.searching import Results
from typing import List, Dict, Any


def search(query_str: str, index_dir: str = 'indexdir', limit: int = None) -> List[Dict[str, Any]]:
    """
    Searches the Whoosh index for documents matching the given query.

    Args:
        query_str (str): The query string to search for.
        index_dir (str, optional): The directory where the Whoosh index is stored. Defaults to 'indexdir'.
        limit (int, optional): The maximum number of results to return. Defaults to None, which returns all results.

    Returns:
        List[Dict[str, Any]]: A list of search results, where each result is a dictionary of field values.
    """
    ix = open_dir(index_dir)
    
    with ix.searcher() as searcher:
        query_parser = MultifieldParser(
            ["numer_ksiegi", "typ_ksiegi", "oznaczenie_wydzialu", "polozanie", "wlasciciel"],
            ix.schema
        )
        query_parser.add_plugin(FuzzyTermPlugin()) 
        query: Query = query_parser.parse(query_str)

        results: Results = searcher.search(query, limit=limit)

        return [dict(result) for result in results]