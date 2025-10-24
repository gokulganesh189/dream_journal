from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.logger import get_logger
import time

logger = get_logger("request_logger")

class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP request and response details.
    - SRP: Logs request and response only.
    - OCP: Extendable for different log sinks (DB, external services).
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Read body safely (works for both JSON and form-data)
        body_bytes = await request.body()
        content_type = request.headers.get("content-type", "")

        # Handle request logging safely
        if "multipart/form-data" in content_type:
            body_preview = f"<multipart form-data, {len(body_bytes)} bytes>"
        else:
            try:
                body_preview = body_bytes.decode("utf-8")
            except UnicodeDecodeError:
                body_preview = f"<non-UTF8 body, {len(body_bytes)} bytes>"

        logger.info(
            f"REQUEST {request.method} {request.url.path} "
            f"Headers={dict(request.headers)} "
            f"Body={body_preview}"
        )

        # Call downstream
        response: Response = await call_next(request)

        process_time = (time.time() - start_time) * 1000  # ms

        # Intercept response body to log it
        resp_body = b""
        async for chunk in response.body_iterator:
            resp_body += chunk

        # Reconstruct the response
        new_response = Response(
            content=resp_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        # Safe decode response too
        resp_content_type = response.headers.get("content-type", "")
        if "application/json" in resp_content_type or "text" in resp_content_type:
            try:
                resp_preview = resp_body.decode("utf-8")
            except UnicodeDecodeError:
                resp_preview = f"<non-UTF8 response, {len(resp_body)} bytes>"
        else:
            resp_preview = f"<binary response, {len(resp_body)} bytes>"

        logger.info(
            f"RESPONSE {request.method} {request.url.path} "
            f"Status={response.status_code} "
            f"Time={process_time:.2f}ms "
            f"Body={resp_preview}"
        )

        return new_response
