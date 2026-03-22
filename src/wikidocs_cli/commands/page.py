import click

from wikidocs_cli.utils import print_json, resolve_content


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
@click.option("--content", default=None, help="Page content.")
@click.option("--file", "file_path", type=click.Path(exists=True), default=None, help="Read content from file.")
@click.option("--book-id", type=int, default=None, help="Book to add the page to (use 'book list' to find your book ID).")
@click.option("--parent-id", type=int, default=None, help="Parent page ID.")
@click.option("--open", "is_open", is_flag=True, help="Make the page public.")
@click.pass_context
def page_create(ctx, subject, content, file_path, book_id, parent_id, is_open):
    """Create a new page. Returns JSON including the created page's id."""
    from wikidocs_cli.main import get_client
    content = resolve_content(content, file_path)
    data = get_client(ctx).create_page(subject, content, book_id=book_id, parent_id=parent_id, is_open=is_open)
    print_json(data)


@page.command("update")
@click.argument("page_id", type=int)
@click.option("--subject", required=True, help="Page title.")
@click.option("--content", default=None, help="Page content.")
@click.option("--file", "file_path", type=click.Path(exists=True), default=None, help="Read content from file.")
@click.option("--parent-id", type=int, default=None, help="Parent page ID.")
@click.option("--open", "is_open", is_flag=True, help="Make the page public.")
@click.pass_context
def page_update(ctx, page_id, subject, content, file_path, parent_id, is_open):
    """Update an existing page."""
    from wikidocs_cli.main import get_client
    content = resolve_content(content, file_path)
    data = get_client(ctx).update_page(page_id, subject, content, parent_id=parent_id, is_open=is_open)
    print_json(data)
