import click

from wikidocs_cli.utils import print_json


@click.group()
def page():
    """Manage WikiDocs pages."""


@page.command("get")
@click.argument("page_id", type=int)
@click.pass_context
def page_get(ctx, page_id):
    """Get a page by ID."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).get_page(page_id)
    print_json(data)


@page.command("create")
@click.option("--subject", required=True, help="Page title.")
@click.option("--content", required=True, help="Page content.")
@click.option("--book-id", type=int, default=None, help="Book to add the page to.")
@click.option("--parent-id", type=int, default=None, help="Parent page ID.")
@click.option("--open", "is_open", is_flag=True, help="Make the page public.")
@click.pass_context
def page_create(ctx, subject, content, book_id, parent_id, is_open):
    """Create a new page."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).create_page(subject, content, book_id=book_id, parent_id=parent_id, is_open=is_open)
    print_json(data)


@page.command("update")
@click.argument("page_id", type=int)
@click.option("--subject", required=True, help="Page title.")
@click.option("--content", required=True, help="Page content.")
@click.option("--book-id", type=int, default=None, help="Book ID.")
@click.option("--parent-id", type=int, default=None, help="Parent page ID.")
@click.option("--open", "is_open", is_flag=True, help="Make the page public.")
@click.pass_context
def page_update(ctx, page_id, subject, content, book_id, parent_id, is_open):
    """Update an existing page."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).update_page(page_id, subject, content, book_id=book_id, parent_id=parent_id, is_open=is_open)
    print_json(data)
