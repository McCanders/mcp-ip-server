import os
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
    """Basic health check for Railway monitoring."""
    return JSONResponse({"status": "healthy", "mcp": "active"})

# 2. Use the built-in mcp.lifespan in the Starlette constructor
app = Starlette(
    lifespan=mcp.lifespan, 
    routes=[
        Route("/", endpoint=health_check),
    ],
)

# 3. Mount the HTTP app (stateless by default in v3.0)
app.mount("/", mcp.http_app(transport="http"))

if __name__ == "__main__":
    # Railway provides the port via an environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)