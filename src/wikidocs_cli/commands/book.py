import click

from wikidocs_cli.utils import print_json, print_table


@click.group()
def book():
    """Manage WikiDocs books."""


@book.command("list")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def book_list(ctx, as_json):
    """List your books."""
    data = ctx.obj.list_books()
    if as_json:
        print_json(data)
    else:
        books = data if isinstance(data, list) else data.get("results", data.get("books", [data]))
        print_table(books, ["id", "subject"])


@book.command("get")
@click.argument("book_id", type=int)
@click.pass_context
def book_get(ctx, book_id):
    """Get details of a book."""
    data = ctx.obj.get_book(book_id)
    print_json(data)


@book.command("create")
@click.option("--subject", required=True, help="Book title.")
@click.option("--summary", default=None, help="Book summary.")
@click.option("--open", "is_open", is_flag=True, help="Make the book public.")
@click.option("--image", "image_path", type=click.Path(exists=True), default=None, help="Cover image file.")
@click.pass_context
def book_create(ctx, subject, summary, is_open, image_path):
    """Create a new book."""
    data = ctx.obj.create_book(subject, summary=summary, is_open=is_open, image_path=image_path)
    print_json(data)
