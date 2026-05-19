from typing import cast
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


def _request_meta(request: Request) -> dict:
    return {
        "path": request.url.path,
        "method": request.method,
        "request_id": request.headers.get("X-Request-ID"),
    }


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    validation_exc = cast(RequestValidationError, exc)
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "Success": False,
            "message": "Validation Error",
            "errors": validation_exc.errors(),
            "meta": _request_meta(request),
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal Server Error",
            "meta": _request_meta(request),
        },
    )
