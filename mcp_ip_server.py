from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
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

sse = SseServerTransport("/messages/")

async def handle_sse(request: Request):
    ip = (
        request.headers.get("x-forwarded-for", "").split(",")[0].strip()
        or request.headers.get("x-real-ip")
        or request.client.host
    )
    caller_ip.set(ip)
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

if __name__ == "__main__":
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)
```
- Click **"Commit new file"** ✅

---

**3. Create `requirements.txt`:**
- Click **"Add file"** → **"Create new file"**
- Name it `requirements.txt`
- Paste:
```
mcp
uvicorn
starlette
httpx
```
- Click **"Commit new file"** ✅

---

**4. Create `Procfile`:**
- Click **"Add file"** → **"Create new file"**
- Name it `Procfile` (no extension!)
- Paste:
```
web: uvicorn mcp_ip_server:starlette_app --host 0.0.0.0 --port $PORT
