import os
import uvicorn
import contextlib
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 1. Initialize FastMCP 3.0
mcp = FastMCP("GeoLocation-APP")

@mcp.tool()
async def get_my_ip() -> str:
    """Returns a success message to verify connectivity."""
    return "Successfully connected to Railway MCP server using FastMCP 3.0."

async def health_check(request):
    """Health check for Railway monitoring."""
    return JSONResponse({"status": "healthy", "mcp": "active"})

# 2. Wrapper to handle the Starlette app argument for lifespan
@contextlib.asynccontextmanager
async def lifespan_wrapper(app: Starlette):
    async with mcp.lifespan():
        yield

app = Starlette(
    lifespan=lifespan_wrapper, 
    routes=[
        Route("/", endpoint=health_check),
    ],
)

# 3. CRITICAL: Pass path="/" to ensure /tools and /tools/call are at the root
# transport="http" is required for Copilot Studio
mcp_handler = mcp.http_app(transport="http", path="/") 
app.mount("/", mcp_handler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
