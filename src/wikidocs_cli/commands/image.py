import click

from wikidocs_cli.utils import print_json


@click.group()
def image():
    """Manage WikiDocs images."""


@image.command("upload")
@click.option("--page-id", type=int, required=True, help="Page to attach the image to.")
@click.option("--file", "file_path", type=click.Path(exists=True), required=True, help="Image file to upload.")
@click.pass_context
def image_upload(ctx, page_id, file_path):
    """Upload an image to a page."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).upload_image(page_id, file_path)
    print_json(data)
