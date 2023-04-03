from typing import Dict, List, Optional
from pathlib import Path
import importlib.resources as pkg_resources
import json
import requests
from random import choice

from .types import Tag, Author, Quote
from .helper import EnhancedJSONDecoder, EnhancedJSONEncoder, urljoin, QuoteNotFound, create_query

DEFAULT_CATALOG = 'data/default-catalog.json'
class QuoteCatalog():
    def __init__(self, catalog_path:Optional[Path]=None, base_api_url:str="https://api.quotable.io/"):
        """Provides an interface with a quote server and a local database

        Args:
            catalog_path (Optional[Path], optional): A user provided path to an alternate local catalog. Defaults to None.
            base_api_url (str, optional): Base API Url to remote server holding quotes. Defaults to "https://api.quotable.io/".
        """
        self.custom_catalog_path = catalog_path
        # assign the urls for the api server
        self.base_api_url:str=base_api_url
        self.tag_url:str = urljoin(self.base_api_url, "tags") # https://api.quotable.io/tags
        self.author_url:str = urljoin(self.base_api_url, "authors") # https://api.quotable.io/authors
        self.random_url:str = urljoin(self.base_api_url, "random") # https://api.quotable.io/random

        # a dictionary of all available tags, authors, and quotes that can be queried
        self.available_tags: Dict[str, Tag] = {}
        self.available_authors: Dict[str, Author] = {}
        self.available_quotes: Dict[str, Quote] = {}

        # load data from catalog
        self.load_data()

    def __del__(self):
        """Save all data to local catalog on exit"""
        self.save_data()
    
    def refresh_tags(self):
        """Queries the API server to get all tags"""
        # clear existing tags
        self.available_tags = {}
        # request new data from api
        data = requests.get(self.tag_url).json()
        # create new tags from the data
        for tag_data in data:
            tag = Tag.from_dict(tag_data)
            self.available_tags[tag.name] = tag

    def refresh_authors(self):
        """Queries the API server to get all authors"""
        self.available_authors = {} # clear existing tags
        url = self.author_url + create_query(limit=150)
        data = requests.get(url).json() # request new data from api
        # create new tags from the data
        for author_data in data['results']:
            author = Author.from_dict(author_data)
            self.available_authors[author.slug] = author
        # TODO - Get all the pages, not just one
    
    def get_available_tags(self) -> List[Tag]:
        """Will get all tags available for query"""
        if len(self.available_tags) == 0:
            self.refresh_tags()
        return self.available_tags
    
    def get_available_authors(self) -> List[Tag]:
        """Will get all authors available for query"""
        if len(self.available_authors) == 0:
            self.refresh_authors()
        return self.available_authors
    
    def load_data(self):
        """Loads data from catalog"""
        catalog_path = self.custom_catalog_path
        if catalog_path is None:
            catalog_path = pkg_resources.as_file(pkg_resources.files('qotd').joinpath(DEFAULT_CATALOG))
        with catalog_path as path:
            with open(path, 'r') as fp:
                data:dict = json.load(fp, cls=EnhancedJSONDecoder)
            self.available_authors.update(data.get('available_authors', {}))
            self.available_quotes.update(data.get('available_quotes', {}))
            self.available_tags.update(data.get('available_tags', {}))

    def save_data(self):
        """Saves data to catalog"""
        catalog_path = self.custom_catalog_path
        if catalog_path is None:
            catalog_path = pkg_resources.as_file(pkg_resources.files('qotd').joinpath(DEFAULT_CATALOG))
        with catalog_path as path:
            data = dict(available_authors=self.available_authors,
                        available_quotes=self.available_quotes,
                        available_tags=self.available_tags)
            with open(path, 'w') as fp:
                json.dump(data, fp, cls=EnhancedJSONEncoder, indent=4)
    
    def get_random_quote(self, tags:List[Tag] = [], and_tags=False, authors:List[Author]= [], use_cache=False) -> Quote:
        if use_cache:
            # TODO, do python filtering here
            return choice(list(self.available_quotes.values()))
        else:
            url = self.random_url +  create_query(tags=tags, and_tags=and_tags, authors=authors)
            data = requests.get(url).json()
            if 'statusCode' in data:
                raise QuoteNotFound
            # create quote
            new_quote = Quote(author=data['author'], content=data['content'], tags=data['tags'], _id=data["_id"])
            # update catalog of quotes
            self.available_quotes[new_quote._id] = new_quote
            return new_quote # return quote
    

def main():
    qc = QuoteCatalog()
    qc.load_data()
    tags = qc.get_available_tags()
    print(tags)

if __name__ == "__main__":
    main()

    


    