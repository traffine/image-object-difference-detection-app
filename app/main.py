import uvicorn
from api.routes.api import router as api_router
from core.config import DEBUG, PROJECT_NAME, VERSION
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response
from mangum import Mangum
from starlette.requests import Request


def get_application() -> FastAPI:
    """
    FastAPI config

    Args:

    Returns:
        FastAPI
    """
    application = FastAPI(
        title=PROJECT_NAME,
        version=VERSION,
        debug=DEBUG,
    )
    application.include_router(api_router)
    return application


app = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request):
    """
    Customize response to FastAPI errors

    Args:
        request (Request): Request

    Returns:
        Response
    """
    return Response(status_code=500)


def custom_openapi():
    """
    Remove FastAPI's OpenAPI 422 error

    Args:

    Returns:
        fastapi.openapi
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
    for method in openapi_schema["paths"]:
        try:
            del openapi_schema["paths"][method]["post"]["responses"]["422"]
        except KeyError:
            pass
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)
