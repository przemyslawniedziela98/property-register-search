import re 
from typing import List, Dict, Any
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin


def extract_data_from_io_dep(io_dep_text: str) -> Dict[str, List[str]]:
    """
    Extract parcel numbers and locations from the IO department section of a land registry document.

    Args:
        io_dep_text (str): The text from the IO department section of the land registry document.

    Returns:
        Dict[str, List[str]]: A dictionary containing list of parcel numbers and locations
    """
    first_occurrence = lambda t: t[0] if len(t) > 0 else ""
    parcel_numbers = re.findall(r"Numer działki \d+", io_dep_text)
    location_pattern = r"Położenie \(numer porządkowy / województwo, gmina, miejscowość\).*?(\d+ )?"
    locations = re.findall(location_pattern, io_dep_text)
    return {'number': first_occurrence(parcel_numbers), 
            'location': first_occurrence(locations)}

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
            ["numer_ksiegi", "typ_ksiegi", "oznaczenie_wydzialu", "polozanie", "wlasciciel", "dzial_i_o"],
            ix.schema
        )
        query_parser.add_plugin(FuzzyTermPlugin()) 
        query = query_parser.parse(query_str)

        results = searcher.search(query, limit=limit)
        
        extended_results = []
        for result in results: 
            result = dict(result)
            result.update(extract_data_from_io_dep(result['dzial_i_o']))
            extended_results.append(result)
        return extended_results