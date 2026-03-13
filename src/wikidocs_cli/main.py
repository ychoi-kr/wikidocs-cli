import click

from wikidocs_cli.client import WikiDocsClient
from wikidocs_cli.commands.book import book
from wikidocs_cli.commands.page import page
from wikidocs_cli.commands.image import image
from wikidocs_cli.commands.blog import blog


@click.group()
@click.option(
    "--token",
    envvar="WIKIDOCS_TOKEN",
    required=True,
    help="WikiDocs API token (or set WIKIDOCS_TOKEN env var).",
)
@click.pass_context
def cli(ctx, token):
    """WikiDocs CLI — manage books, pages, images, and blog posts."""
    ctx.ensure_object(dict)
    ctx.obj = WikiDocsClient(token)


cli.add_command(book)
cli.add_command(page)
cli.add_command(image)
cli.add_command(blog)
