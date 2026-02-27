import os
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
import contextlib

# CRITICAL: stateless_http=True is required for Copilot Studio
mcp = FastMCP("GeoLocation-APP", stateless_http=True)

@mcp.tool()
async def get_my_ip() -> str:
    """
    Returns a success message to verify the MCP connection is working.
    In cloud environments, actual client IP detection requires specific header parsing.
    """
    return "Successfully connected to Railway MCP server."

# Basic health check for Railway deployment monitoring
async def health_check(request):
    return JSONResponse({"status": "healthy", "mcp": "active"})

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

# Create the Starlette app
app = Starlette(
    lifespan=lifespan,
    routes=[
        Route("/", endpoint=health_check),
    ],
)

# Mount the MCP endpoints (tools, tools/call) at the root
app.mount("/", mcp.streamable_http_app())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)