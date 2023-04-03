import json
from dataclasses import asdict, is_dataclass
from .types import Author, Quote, Tag
from typing import List, Optional


class QuoteNotFound(Exception):
    """Quote not found in API Server"""
    def __init__(self, message="Quote not found in API Server"):
        self.message = message
        super().__init__(self.message)

def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return "/".join(map(lambda x: str(x).rstrip('/'), args))

class EnhancedJSONEncoder(json.JSONEncoder):
    """This will allow the encoding of our custom dataclasses"""
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)

class EnhancedJSONDecoder(json.JSONDecoder):
    """This will allow the decoding of our custom dataclasses"""
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    def object_hook(self, data):
        # These are all the available keys we want to transform
        object_keys = {'available_authors': Author, 'available_quotes': Quote, 'available_tags': Tag}
        for resource_key, cls in object_keys.items():
            # if this data is available
            if resource_key in data:
                # go through every key and transform the value to the appropriate class
                for key, value in data[resource_key].items():
                    data[resource_key][key] = cls.from_dict(value)
        return data
    

def create_query(tags:List[Tag] = [], and_tags=False, authors:List[Author]= [], limit:Optional[int]=None) -> str:
    """This will create a query string given a list of parameters

    Args:
        tags (List[Tag], optional): A list of all tags to constrain our query by. Defaults to [].
        and_tags (bool, optional): If True, will require all tags to be present in the query. Defaults to False.
        authors (List[Author], optional): A list of all authors to constrain our query. Defaults to [].
        limit (Optional[int], optional): A maximum of how many entities should be returned. Defaults to None.

    Returns:
        str: The query string
    """
    url = '?'
    if tags:
        join_str = "," if and_tags else "|" # ',' denotes AND, | denotes OR
        tag_str = join_str.join([tag.name for tag in tags])
        url += f"tags={tag_str}"
    if authors:
        author_str = "|".join([author.slug for author in authors])
        url += f"&author={author_str}"
    if limit:
        url += f"&limit={limit}"
    return url
