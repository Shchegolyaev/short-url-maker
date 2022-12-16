import uvicorn as uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse

from api.v1 import base
from core.config import app_settings

app = FastAPI(
    title=app_settings.app_title,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(base.router, prefix="/api/v1")

BLACKLISTED_IPS = []


@app.middleware("http")
async def validate_ip(request: Request, call_next):
    # Get client IP
    ip = str(request.client.host)

    if ip in BLACKLISTED_IPS:
        data = {"message": f"IP {ip} is not allowed to access this resource."}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=data)
    # Proceed if IP is allowed
    return await call_next(request)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.project_host,
        port=app_settings.project_port,
    )
