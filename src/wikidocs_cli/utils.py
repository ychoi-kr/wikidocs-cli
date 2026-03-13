import json


def print_json(data):
    click_echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_table(rows: list[dict], headers: list[str]):
    if not rows:
        click_echo("No results.")
        return

    col_widths = {h: len(h) for h in headers}
    str_rows = []
    for row in rows:
        str_row = {h: str(row.get(h, "")) for h in headers}
        for h in headers:
            col_widths[h] = max(col_widths[h], len(str_row[h]))
        str_rows.append(str_row)

    header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
    click_echo(header_line)
    click_echo("  ".join("-" * col_widths[h] for h in headers))
    for str_row in str_rows:
        click_echo("  ".join(str_row[h].ljust(col_widths[h]) for h in headers))


def click_echo(msg: str):
    import click
    click.echo(msg)
