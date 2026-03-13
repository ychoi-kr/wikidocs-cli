import click
import requests


class WikiDocsClient:
    def __init__(self, token: str):
        self.base_url = "https://wikidocs.net/napi"
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {token}"})

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.session.request(method, url, **kwargs)
        if not resp.ok:
            try:
                detail = resp.json()
            except Exception:
                detail = resp.text
            raise click.ClickException(
                f"API error {resp.status_code}: {detail}"
            )
        return resp.json()

    # --- Books ---

    def list_books(self) -> dict:
        return self._request("GET", "/books/")

    def get_book(self, book_id: int) -> dict:
        return self._request("GET", f"/books/{book_id}/")

    def create_book(
        self,
        subject: str,
        summary: str | None = None,
        is_open: bool = False,
        image_path: str | None = None,
    ) -> dict:
        data = {"subject": subject}
        if summary is not None:
            data["summary"] = summary
        if is_open:
            data["is_open"] = "true"
        files = None
        if image_path is not None:
            files = {"image": open(image_path, "rb")}
        try:
            return self._request("POST", "/books/create/", data=data, files=files)
        finally:
            if files:
                files["image"].close()

    # --- Pages ---

    def get_page(self, page_id: int) -> dict:
        return self._request("GET", f"/pages/{page_id}/")

    def create_page(
        self,
        subject: str,
        content: str,
        book_id: int | None = None,
        parent_id: int | None = None,
        is_open: bool = False,
    ) -> dict:
        payload: dict = {"subject": subject, "content": content}
        if book_id is not None:
            payload["book_id"] = book_id
        if parent_id is not None:
            payload["parent_id"] = parent_id
        if is_open:
            payload["is_open"] = True
        return self._request("POST", "/pages/create/", json=payload)

    def update_page(
        self,
        page_id: int,
        subject: str,
        content: str,
        book_id: int | None = None,
        parent_id: int | None = None,
        is_open: bool = False,
    ) -> dict:
        payload: dict = {"id": page_id, "subject": subject, "content": content}
        if book_id is not None:
            payload["book_id"] = book_id
        if parent_id is not None:
            payload["parent_id"] = parent_id
        if is_open:
            payload["is_open"] = True
        return self._request("PUT", f"/pages/{page_id}/", json=payload)

    # --- Images ---

    def upload_image(self, page_id: int, file_path: str) -> dict:
        data = {"page_id": page_id}
        files = {"file": open(file_path, "rb")}
        try:
            return self._request("POST", "/images/upload/", data=data, files=files)
        finally:
            files["file"].close()

    # --- Blog ---

    def blog_profile(self) -> dict:
        return self._request("GET", "/blog/profile/")

    def blog_list(self, page: int = 1) -> dict:
        return self._request("GET", f"/blog/list/{page}")

    def blog_get(self, blog_id: int) -> dict:
        return self._request("GET", f"/blog/{blog_id}")

    def blog_create(
        self,
        title: str,
        content: str,
        is_public: bool = False,
        tags: str | None = None,
    ) -> dict:
        result = self._request("POST", "/blog/create/", data={})
        blog_id = result["id"]
        return self.blog_update(blog_id, title, content, is_public=is_public, tags=tags)

    def blog_update(
        self,
        blog_id: int,
        title: str,
        content: str,
        is_public: bool = False,
        tags: str | None = None,
    ) -> dict:
        payload: dict = {
            "title": title,
            "content": content,
            "is_public": is_public,
            "tags": tags or "",
        }
        return self._request("PUT", f"/blog/{blog_id}/", json=payload)

    def blog_upload_image(self, blog_id: int, file_path: str) -> dict:
        data = {"blog_id": blog_id}
        files = {"file": open(file_path, "rb")}
        try:
            return self._request("POST", "/blog/images/upload/", data=data, files=files)
        finally:
            files["file"].close()
