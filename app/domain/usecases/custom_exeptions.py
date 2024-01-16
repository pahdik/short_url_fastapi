class DuplicateEntryError(Exception):
    def __init__(self, detail: str = "Duplicate entry"):
        super().__init__(detail)
        self.status_code = 409
        self.detail = detail


class NotFoundError(Exception):
    def __init__(self, detail: str = "Not found"):
        super().__init__(detail)
        self.status_code = 404
        self.detail = detail
