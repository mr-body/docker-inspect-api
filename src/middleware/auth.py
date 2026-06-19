from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.util.auth import decode_access_token

async def auth_middleware(request: Request, call_next):
    excluded_paths = ["/auth/login", "/health", "/docs", "/openapi.json", "/ui"]

    # Allow CORS preflight requests through without auth
    if request.method == "OPTIONS":
        return await call_next(request)

    if any(request.url.path.startswith(path) for path in excluded_paths):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Missing or invalid Authorization header"})

    token = auth_header.split(" ")[1]
    decoded = decode_access_token(token)
    if not decoded:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    request.state.user = decoded.get("sub")
    return await call_next(request)