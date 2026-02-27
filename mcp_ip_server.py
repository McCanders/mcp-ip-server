from mcp.server import Server
from mcp.server.streamable_http import StreamableHTTPServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
import uvicorn
import contextvars

caller_ip: contextvars.ContextVar[str] = contextvars.ContextVar("caller_ip", default="unknown")

app = Server("ip-address-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_my_ip",
            description="Returns the caller's IP address",
            inputSchema={"type": "object", "properties": {}, "required": []}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_my_ip":
        ip = caller_ip.get()
        return [TextContent(type="text", text=f"Your IP address is: {ip}")]
    raise ValueError(f"Unknown tool: {name}")

async def handle_mcp(request: Request):
    ip = (
        request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        or request.headers.get("x-real-ip")
        or request.client.host
    )
    caller_ip.set(ip)
    transport = StreamableHTTPServerTransport("/mcp")
    async with transport.connect(request) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

starlette_app = Starlette(
    routes=[
        Route("/mcp", endpoint=handle_mcp, methods=["GET", "POST"]),
    ]
)

if __name__ == "__main__":
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)