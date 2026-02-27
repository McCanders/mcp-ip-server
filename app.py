import os
import uvicorn
from fastmcp import FastMCP

# 1. Initialize FastMCP 3.0
mcp = FastMCP("GeoLocation-APP")

@mcp.tool()
async def get_my_ip() -> str:
    """Returns a success message to verify connectivity."""
    return "Successfully connected to Railway MCP server using FastMCP 3.0."

# 2. In v3.0, the cleanest way to avoid 502 errors on Railway is to 
# use the mcp.http_app() directly as your main application.
# 'stateless_http=True' is the standard for cloud deployment.
app = mcp.http_app(transport="http", stateless_http=True)

# 3. Add a simple health check directly to the MCP app if needed
@app.get("/")
async def health():
    return {"status": "healthy", "mcp": "active"}

if __name__ == "__main__":
    # Railway provides the port via an environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
