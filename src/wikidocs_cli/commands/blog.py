import click

from wikidocs_cli.utils import print_json, print_table


@click.group()
def blog():
    """Manage WikiDocs blog posts."""


@blog.command("profile")
@click.pass_context
def blog_profile(ctx):
    """Get your blog profile."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).blog_profile()
    print_json(data)


@blog.command("list")
@click.option("--page", "page_num", type=int, default=1, help="Page number.")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def blog_list(ctx, page_num, as_json):
    """List blog posts."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).blog_list(page_num)
    if as_json:
        print_json(data)
    else:
        posts = data if isinstance(data, list) else data.get("blog_pages", data.get("results", data.get("posts", [data])))
        print_table(posts, ["id", "title"])


@blog.command("get")
@click.argument("blog_id", type=int)
@click.pass_context
def blog_get(ctx, blog_id):
    """Get a blog post by ID."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).blog_get(blog_id)
    print_json(data)


@blog.command("create")
@click.option("--title", required=True, help="Blog post title.")
@click.option("--content", required=True, help="Blog post content.")
@click.option("--public", "is_public", is_flag=True, help="Make the post public.")
@click.option("--tags", default=None, help="Comma-separated tags.")
@click.pass_context
def blog_create(ctx, title, content, is_public, tags):
    """Create a new blog post. Returns JSON including the created post's id."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).blog_create(title, content, is_public=is_public, tags=tags)
    print_json(data)


@blog.command("update")
@click.argument("blog_id", type=int)
@click.option("--title", required=True, help="Blog post title.")
@click.option("--content", required=True, help="Blog post content.")
@click.option("--public", "is_public", is_flag=True, help="Make the post public.")
@click.option("--tags", default=None, help="Comma-separated tags.")
@click.pass_context
def blog_update(ctx, blog_id, title, content, is_public, tags):
    """Update a blog post."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).blog_update(blog_id, title, content, is_public=is_public, tags=tags)
    print_json(data)


@blog.command("image-upload")
@click.option("--blog-id", type=int, required=True, help="Blog post ID.")
@click.option("--file", "file_path", type=click.Path(exists=True), required=True, help="Image file to upload.")
@click.pass_context
def blog_image_upload(ctx, blog_id, file_path):
    """Upload an image to a blog post."""
    from wikidocs_cli.main import get_client
    data = get_client(ctx).blog_upload_image(blog_id, file_path)
    print_json(data)
