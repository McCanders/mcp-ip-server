import os
import uvicorn
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 1. Initialize FastMCP
mcp = FastMCP("GeoLocation-APP")

@mcp.tool()
async def get_my_ip() -> str:
    """Returns a success message to verify connectivity."""
    return "Successfully connected to Railway MCP server using FastMCP 3.0."

async def health_check(request):
    return JSONResponse({"status": "healthy", "mcp": "active"})

# 2. Create the MCP app instance first
# stateless_http=True and path="/" are critical for Copilot Studio
mcp_app = mcp.http_app(transport="streamable-http", stateless_http=True, path="/")

# 3. Use the MCP app's own lifespan for the Starlette parent
app = Starlette(
    lifespan=mcp_app.lifespan, 
    routes=[
        Route("/", endpoint=health_check),
    ],
)

# 4. Mount the MCP app at the root
app.mount("/", mcp_app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
