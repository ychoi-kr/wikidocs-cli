import click

from wikidocs_cli.client import WikiDocsClient
from wikidocs_cli.config import load_token, save_token, remove_token, CREDENTIALS_FILE
from wikidocs_cli.commands.book import book
from wikidocs_cli.commands.page import page
from wikidocs_cli.commands.image import image
from wikidocs_cli.commands.blog import blog


@click.group()
@click.option(
    "--token",
    envvar="WIKIDOCS_TOKEN",
    default=None,
    help="WikiDocs API token (overrides stored credentials).",
)
@click.option(
    "--profile",
    default="default",
    help="Named profile in ~/.wikidocs/credentials.",
)
@click.pass_context
def cli(ctx, token, profile):
    """WikiDocs CLI — manage books, pages, images, and blog posts."""
    ctx.ensure_object(dict)
    ctx.obj = {"token": token, "profile": profile}


def get_client(ctx):
    """Get or create a WikiDocsClient from the Click context."""
    obj = ctx.find_root().obj
    if isinstance(obj, dict):
        token = obj.get("token")
        profile = obj.get("profile", "default")
        if not token:
            token = load_token(profile)
        if not token:
            raise click.ClickException(
                "No API token found. Run 'wikidocs configure' to set up credentials."
            )
        client = WikiDocsClient(token)
        ctx.find_root().obj = client
        return client
    return obj


cli.add_command(book)
cli.add_command(page)
cli.add_command(image)
cli.add_command(blog)


# --- configure command ---

@cli.command()
@click.option("--token", "input_token", default=None, help="API token (non-interactive).")
@click.pass_context
def configure(ctx, input_token):
    """Set up WikiDocs API credentials."""
    profile = ctx.find_root().obj.get("profile", "default")
    if input_token is None:
        input_token = click.prompt("WikiDocs API token", hide_input=True)
    save_token(input_token, profile)
    click.echo(f"Credentials saved to {CREDENTIALS_FILE} [profile: {profile}]")


@cli.command()
@click.pass_context
def logout(ctx):
    """Remove stored WikiDocs credentials."""
    profile = ctx.find_root().obj.get("profile", "default")
    remove_token(profile)
    click.echo(f"Credentials removed for profile: {profile}")


# --- help-all command ---

def _collect_help(group, prefix="wikidocs"):
    """Recursively collect help text from all commands."""
    lines = []
    ctx = click.Context(group, info_name=prefix)
    formatter = ctx.make_formatter()
    group.format_help(ctx, formatter)
    lines.append(f"{'=' * 60}")
    lines.append(f"  {prefix}")
    lines.append(f"{'=' * 60}")
    lines.append(formatter.getvalue().rstrip())
    lines.append("")

    if hasattr(group, "list_commands"):
        for cmd_name in group.list_commands(ctx):
            cmd = group.get_command(ctx, cmd_name)
            if cmd is None:
                continue
            sub_prefix = f"{prefix} {cmd_name}"
            if isinstance(cmd, click.Group):
                lines.extend(_collect_help(cmd, sub_prefix))
            else:
                sub_ctx = click.Context(cmd, info_name=cmd_name, parent=ctx)
                formatter = sub_ctx.make_formatter()
                cmd.format_help(sub_ctx, formatter)
                lines.append(f"{'=' * 60}")
                lines.append(f"  {sub_prefix}")
                lines.append(f"{'=' * 60}")
                lines.append(formatter.getvalue().rstrip())
                lines.append("")

    return lines


@cli.command("help-all")
def help_all():
    """Show help for all commands at once."""
    lines = _collect_help(cli)
    click.echo("\n".join(lines))
