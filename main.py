import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from app.domain.usecases.custom_exeptions import DuplicateEntryError
from app.infrastucture.api.v0 import url_router

app = FastAPI()

@app.exception_handler(DuplicateEntryError)
async def duplicate_entry_error_handler(request: Request, exc: DuplicateEntryError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Incorrect data"
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content="Incorrect data"
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="Internal server error"
    )


app.include_router(url_router.router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
