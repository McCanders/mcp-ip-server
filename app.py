import os
import contextlib
import uvicorn
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 1. Initialize the FastMCP 3.0 server
mcp = FastMCP("GeoLocation-APP")

@mcp.tool()
async def get_my_ip() -> str:
    """Returns a success message to verify connectivity."""
    return "Successfully connected to Railway MCP server using FastMCP 3.0."

async def health_check(request):
    return JSONResponse({"status": "healthy", "mcp": "active"})

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    # Required for v3.0 to initialize tools and providers
    async with mcp.session_manager.run():
        yield

app = Starlette(
    lifespan=lifespan,
    routes=[
        Route("/", endpoint=health_check),
    ],
)

# 2. In v3.0, simply use transport="http". It is stateless by default.
mcp_handler = mcp.http_app(transport="http")
app.mount("/", mcp_handler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)