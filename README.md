# wikidocs-cli

Command-line tool for the [WikiDocs](https://wikidocs.net) API. Manage books, pages, images, and blog posts from the terminal.

## Installation

```bash
pip install git+https://github.com/ychoi-kr/wikidocs-cli.git
```

Or install from source:

```bash
git clone https://github.com/ychoi-kr/wikidocs-cli.git
cd wikidocs-cli
pip install -e .
```

## Authentication

Get your API token from [WikiDocs](https://wikidocs.net) and set it as an environment variable:

```bash
export WIKIDOCS_TOKEN="your-token-here"
```

Or pass it directly with `--token`:

```bash
wikidocs --token YOUR_TOKEN book list
```

## Commands

### Books

```bash
# List all your books
wikidocs book list

# List books as JSON
wikidocs book list --json

# Get book details (includes full page tree)
wikidocs book get BOOK_ID

# Create a new book
wikidocs book create --subject "My Book"
wikidocs book create --subject "My Book" --summary "A great book" --open
wikidocs book create --subject "My Book" --image cover.png
```

### Pages

```bash
# Get a page
wikidocs page get PAGE_ID

# Create a page in a book
wikidocs page create --book-id BOOK_ID --subject "Chapter 1" --content "Hello world"

# Create a sub-page under a parent page
wikidocs page create --book-id BOOK_ID --parent-id PARENT_PAGE_ID --subject "Section 1.1" --content "Details"

# Create a public page
wikidocs page create --book-id BOOK_ID --subject "Public Page" --content "Content" --open

# Update a page
wikidocs page update PAGE_ID --subject "Updated Title" --content "Updated content"
```

### Images

```bash
# Upload an image to a page
wikidocs image upload --page-id PAGE_ID --file image.png
```

The response includes the image URL:

```json
{
  "id": 12345,
  "page_id": 333686,
  "image_url": "https://static.wikidocs.net/images/page/333686/image.png"
}
```

### Blog

```bash
# View your blog profile
wikidocs blog profile

# List blog posts
wikidocs blog list
wikidocs blog list --page 2
wikidocs blog list --json

# Get a blog post
wikidocs blog get BLOG_ID

# Create a blog post
wikidocs blog create --title "My Post" --content "Post content"
wikidocs blog create --title "My Post" --content "Post content" --public --tags "python,cli"

# Update a blog post
wikidocs blog update BLOG_ID --title "Updated Title" --content "Updated content"
wikidocs blog update BLOG_ID --title "Title" --content "Content" --public --tags "new,tags"

# Upload an image to a blog post
wikidocs blog image-upload --blog-id BLOG_ID --file photo.jpg
```

## Output Formats

- **Table** (default for `list` commands): human-readable columns
- **JSON** (`--json` flag or default for `get`/`create`/`update`): machine-readable, suitable for piping to `jq`

```bash
# Pipe JSON to jq
wikidocs book list --json | jq '.[].id'
wikidocs page get 12345 | jq -r '.content'
```

## Discovering Commands

All `--help` flags work without authentication, so you can explore the CLI freely:

```bash
wikidocs --help              # Top-level commands
wikidocs book --help         # Book subcommands
wikidocs page create --help  # Specific command options
```

To see every command and option in a single call:

```bash
wikidocs help-all
```

## Usage with AI Agents

This CLI is designed to be used by AI agents (Claude, GPT, etc.) via shell tool calls.

**First call should be `wikidocs help-all`** — it dumps the full command tree (all groups, subcommands, options, and arguments) in one shot, so the agent can plan its calls without trial and error.

### Common Patterns

**Read a page and rewrite it:**

```bash
# 1. Get current content
wikidocs page get PAGE_ID
# 2. Update with new content
wikidocs page update PAGE_ID --subject "Title" --content "New content here"
```

**Publish a document as a WikiDocs book:**

```bash
# 1. Create a book
wikidocs book create --subject "My Guide" --open
# 2. Parse the book ID from the JSON response, then add pages
wikidocs page create --book-id BOOK_ID --subject "Introduction" --content "..." --open
wikidocs page create --book-id BOOK_ID --subject "Chapter 1" --content "..." --open
# 3. Add sub-pages
wikidocs page create --book-id BOOK_ID --parent-id CHAPTER1_PAGE_ID --subject "Section 1.1" --content "..." --open
```

**Write a blog post with an image:**

```bash
# 1. Create the post
wikidocs blog create --title "Today's Report" --content "..." --public
# 2. Upload an image
wikidocs blog image-upload --blog-id BLOG_ID --file chart.png
# 3. Update content to include the image URL from step 2
wikidocs blog update BLOG_ID --title "Today's Report" --content "![Chart](IMAGE_URL)\n\n..." --public
```

### Tips for AI Agents

- Run `wikidocs help-all` once to discover the full CLI surface in a single call.
- `--help` works without a token — safe to call for exploration.
- All `get`, `create`, and `update` commands output JSON to stdout. Parse with `jq` or directly.
- `--content` accepts Markdown. WikiDocs renders it on the site.
- Use `--json` flag on `list` commands to get structured data instead of a table.
- Page content supports full Markdown including headings, lists, code blocks, and images.
- To include images in content, first upload with `image upload`, then reference the returned `image_url` in Markdown.
- `book get BOOK_ID` returns the full page tree with all pages and their hierarchy — useful for understanding book structure before editing.

## License

MIT
