from fastapi import HTTPException


class DuplicateEntryError(Exception):
    def __init__(self, detail: str = "Duplicate entry"):
        super().__init__(detail)
        self.status_code = 409
        self.detail = detail
