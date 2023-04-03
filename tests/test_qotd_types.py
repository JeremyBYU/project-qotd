from qotd.types import Tag, Author, Quote

def test_tag():
    # test Tag creation 
    t1 = Tag("war", "1")
    assert t1.name == "war"
    assert t1._id == "1"

    # test converting to and from dictionaries
    d1 =dict(name="war", _id="1")
    assert t1.to_dict() == d1
    assert Tag.from_dict(d1) == t1

def test_author():
    # test Author creation 
    a1 = Author(name="0", bio="1", description="2", link="3", slug="4", _id="5")
    assert a1.name == "0"
    assert a1.bio == "1"
    assert a1.description == "2"
    assert a1.link == "3"
    assert a1.slug == "4"
    assert a1._id == "5"

    # test converting to and from dictionaries
    d1 = dict(name="0", bio="1", description="2", link="3", slug="4", _id="5")
    assert a1.to_dict() == d1
    assert Author.from_dict(d1) == a1

def test_quote():
    # test Quote creation 
    q1 = Quote(author="0", content="1", tags=["3", "4"], _id="5")
    assert q1.author == "0"
    assert q1.content == "1"
    assert q1.tags == ["3", "4"]
    assert q1._id == "5"

    # test converting to and from dictionaries
    d1 = dict(author="0", content="1", tags=["3", "4"], _id="5")
    assert q1.to_dict() == d1
    assert Quote.from_dict(d1) == q1