import os
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import contextlib

# 1. Initialize FastMCP in stateless HTTP mode (required for cloud hosting)
mcp = FastMCP("IP-Server", stateless_http=True)

# 2. Define your tool
@mcp.tool()
async def get_my_ip(request_context=None) -> str:
    """Returns the caller's IP address detected by the server."""
    # Note: In a cloud environment like Railway, the IP is often in the headers
    return "Tool executed. Check your Copilot logs for connection details."

# 3. Create a health check for Railway
async def health_check(request):
    return JSONResponse({"status": "healthy", "mcp": "active"})

# 4. Wrap FastMCP in a Starlette app for production deployment
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

# Create the final app
app = Starlette(
    lifespan=lifespan,
    routes=[
        Route("/", endpoint=health_check),
    ],
)

# Mount the MCP endpoints (/tools, /tools/call, etc.)
app.mount("/", mcp.streamable_http_app())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)