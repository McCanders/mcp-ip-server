import os
import uvicorn
from fastmcp import FastMCP
from starlette.responses import JSONResponse
from starlette.routing import Route

# 1. Initialize FastMCP 3.0
mcp = FastMCP("GeoLocation-APP")

@mcp.tool()
async def get_my_ip() -> str:
    """Returns a success message to verify connectivity."""
    return "Successfully connected to Railway MCP server using FastMCP 3.0."

# 2. Define a standard Starlette health check function
async def health_check(request):
    return JSONResponse({"status": "healthy", "mcp": "active"})

# 3. Create the app. 
# We add the health check route directly into the constructor.
app = mcp.http_app(
    transport="http", 
    stateless_http=True,
    routes=[Route("/", endpoint=health_check)]
)

if __name__ == "__main__":
    # Railway provides the port via an environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
