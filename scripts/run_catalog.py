from qotd.lib import QuoteCatalog
def main():
    catalog = QuoteCatalog()
    tags = catalog.get_available_tags()
    print("Tags:")
    print(tags)
    authors = catalog.get_available_authors()
    print("\nAuthors:")
    print(authors)
    quote = catalog.get_random_quote(tags=[tags['war']])
    print("\nQuote:")
    print(quote)

if __name__ == "__main__":
    main()