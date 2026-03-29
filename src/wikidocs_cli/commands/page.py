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
@click.option("--subject", default=None, help="Page title.")
@click.option("--content", default=None, help="Page content.")
@click.option("--file", "file_path", type=click.Path(exists=True), default=None, help="Read content from file.")
@click.option("--parent-id", type=int, default=None, help="Parent page ID. Use 0 to detach to root.")
@click.option("--no-parent", is_flag=True, help="Detach page from its parent and move it to root level.")
@click.option("--open/--no-open", "is_open", default=None, help="Set page public or private. Omit to keep current state.")
@click.pass_context
def page_update(ctx, page_id, subject, content, file_path, parent_id, no_parent, is_open):
    """Update an existing page. Only specified fields are changed."""
    from wikidocs_cli.main import get_client

    if no_parent and parent_id is not None:
        raise click.ClickException("Use either --parent-id or --no-parent, not both.")

    detach_parent = no_parent or parent_id == 0
    if parent_id == 0:
        parent_id = None

    content = resolve_content(content, file_path)
    data = get_client(ctx).update_page(
        page_id,
        subject=subject,
        content=content,
        parent_id=parent_id,
        detach_parent=detach_parent,
        is_open=is_open,
    )
    print_json(data)
