import sys
from typing import List
from .lib import QuoteCatalog
import click

@click.group()
@click.option('catalog', '--catalog', type=click.Path(), help="Path to an alternate quote catalog")
@click.pass_context
def cli(ctx, catalog:str = None):
    qc = QuoteCatalog(catalog_path=catalog)
    ctx.ensure_object(dict)
    ctx.obj['qc'] = qc

@cli.command()
@click.pass_context
def show_tags(ctx):
    """Retrieve all tags available for a quote query"""
    print("Getting available tags:")
    qc:QuoteCatalog = ctx.obj['qc']
    tags = qc.get_available_tags()
    tags_str = ",".join(list(tags.keys()))
    print(tags_str)

@cli.command()
@click.pass_context
def show_authors(ctx):
    """Retrieve all authors available for a quote query"""
    print("Getting available authors:")
    qc:QuoteCatalog = ctx.obj['qc']
    authors = qc.get_available_authors()
    authors_str = ",".join(list(authors.keys()))
    print(authors_str)

@cli.command()
@click.option('--tag', '-t', multiple=True)
@click.option('--author', '-a', multiple=True)
@click.option('--and-tag/--no-and-tag', default=False)
@click.pass_context
def random(ctx, tag: List[str] = [], author: List[str] = [], and_tag:bool=False):
    """Retrieve a random quote given possible tag/author constraints"""
    qc:QuoteCatalog = ctx.obj['qc']
    tags = qc.get_available_tags()
    authors = qc.get_available_authors()
    try:
        constrain_tags = [tags[t] for t in tag]
    except KeyError as e:
        click.secho(f"Tag {e} is not valid. See all available tags with: qotd show-tags", fg='red')
        sys.exit(0)
    try:
        constrain_authors = [authors[a] for a in author]
    except KeyError as e:
        click.secho(f"Author {e} is not valid. See all available authors with: qotd show-authors", fg='red')
        sys.exit(0)
    quote = qc.get_random_quote(tags=constrain_tags, authors=constrain_authors, and_tags=and_tag)
    print(quote)
    

