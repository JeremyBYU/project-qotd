from qotd.lib import QuoteCatalog
from qotd.types import Quote
import json
from pathlib import Path
import pytest

catalog_keys = ["available_tags", "available_authors", "available_quotes"]
FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def empty_catalog(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "empty_catalog.json"
    empty = dict(available_tags={}, available_authors={}, available_quotes={})
    with open(fn, 'w') as fp:
        json.dump(empty, fp)
    return fn

@pytest.fixture(scope="session")
def single_catalog():
    return FIXTURES_DIR / "single.json"


@pytest.fixture(scope="session")
def simple_quote():
    return Quote.from_dict(dict(author='1', content='2', tags=['3', '4'], _id='5'))

def test_empty_quote_catalog_creation(empty_catalog):
    qc = QuoteCatalog(catalog_path=empty_catalog)
    for key in catalog_keys:
        assert len(getattr(qc, key).keys()) == 0

def test_single_quote_catalog_creation(single_catalog):
    qc = QuoteCatalog(catalog_path=single_catalog)
    # Ensure that every catalog key is empty
    for key in catalog_keys:
        assert len(getattr(qc, key).keys()) == 1

def test_default_quote_catalog_creation(single_catalog):
    qc = QuoteCatalog()
    # Ensure that every catalog key is empty
    for key in catalog_keys:
        assert len(getattr(qc, key).keys()) >= 1

def test_get_random_quote(httpserver, simple_quote:Quote):
    httpserver.expect_request("/random") \
        .respond_with_json(simple_quote.to_dict())
    qc = QuoteCatalog(base_api_url=httpserver.url_for("/"))
    quote = qc.get_random_quote()
    assert quote == simple_quote

def test_get_random_quote_extra(httpserver, simple_quote:Quote):
    httpserver.expect_request("/random") \
        .respond_with_json(dict(**simple_quote.to_dict(), test=1))
    qc = QuoteCatalog(base_api_url=httpserver.url_for("/"))
    quote = qc.get_random_quote()
    assert quote == simple_quote

def test_get_random_quote_missing(httpserver, simple_quote:Quote):
    with pytest.raises(Exception) as e_info:
        sq = simple_quote.to_dict()
        del sq['author']
        httpserver.expect_request("/random") \
            .respond_with_json(sq)
        qc = QuoteCatalog(base_api_url=httpserver.url_for("/"))
        quote = qc.get_random_quote()
        assert quote == simple_quote
    