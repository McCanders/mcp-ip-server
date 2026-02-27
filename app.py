import os
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Ensure stateless_http is True for Copilot Studio
mcp = FastMCP("GeoLocation-APP", stateless_http=True)

@mcp.tool()
async def get_my_ip() -> str:
    """Returns a simple success message to verify connectivity."""
    return "Connection Successful: MCP Tool invoked by Copilot Studio."

# Create the app and mount the streamable_http handler
app = Starlette()
app.mount("/", mcp.streamable_http_app())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)