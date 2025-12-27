# https://github.com/modelcontextprotocol/python-sdk

# """
# FastMCP quickstart example.

# cd to the `examples/snippets/clients` directory and run:
#     uv run server fastmcp_quickstart stdio
# """

# from mcp.server.fastmcp import FastMCP

# # Create an MCP server
# mcp = FastMCP("Demo")


# # Add an addition tool
# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b


# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"


# # Add a prompt
# @mcp.prompt()
# def greet_user(name: str, style: str = "friendly") -> str:
#     """Generate a greeting prompt"""
#     styles = {
#         "friendly": "Please write a warm, friendly greeting",
#         "formal": "Please write a formal, professional greeting",
#         "casual": "Please write a casual, relaxed greeting",
#     }

#     return f"{styles.get(style, styles['friendly'])} for someone named {name}."

# mcp.run()




# """Example showing lifespan support for startup/shutdown with strong typing."""

# from collections.abc import AsyncIterator
# from contextlib import asynccontextmanager
# from dataclasses import dataclass

# from mcp.server.fastmcp import Context, FastMCP
# from mcp.server.session import ServerSession


# # Mock database class for example
# class Database:
#     """Mock database class for example."""

#     @classmethod
#     async def connect(cls) -> "Database":
#         """Connect to database."""
#         return cls()

#     async def disconnect(self) -> None:
#         """Disconnect from database."""
#         pass

#     def query(self) -> str:
#         """Execute a query."""
#         return "Query result"


# @dataclass
# class AppContext:
#     """Application context with typed dependencies."""

#     db: Database


# @asynccontextmanager
# async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
#     """Manage application lifecycle with type-safe context."""
#     # Initialize on startup
#     db = await Database.connect()
#     try:
#         yield AppContext(db=db)
#     finally:
#         # Cleanup on shutdown
#         await db.disconnect()


# # Pass lifespan to server
# mcp = FastMCP("My App", lifespan=app_lifespan)


# # Access type-safe lifespan context in tools
# @mcp.tool()
# def query_db(ctx: Context[ServerSession, AppContext]) -> str:
#     """Tool that uses initialized resources."""
#     db = ctx.request_context.lifespan_context.db
#     return db.query()


# """Example showing image handling with FastMCP."""
# # 假设你已经安装了所需的依赖：pip install Pillow fastmcp
# from PIL import Image as PILImage
# from mcp.server.fastmcp import FastMCP, Image

# # 实例化 FastMCP 服务器
# mcp = FastMCP("Image Example")

# @mcp.tool()
# def create_thumbnail(image_path: str) -> Image:
#     """Create a thumbnail from an image.
    
#     The input must be a valid local file path to an image (e.g., 'input.jpg').
#     """
#     try:
#         img = PILImage.open(image_path)
#         img.thumbnail((100, 100))
#         # 返回 MCP 的 Image 对象，格式为 PNG
#         return Image(data=img.tobytes(), format="png")
#     except FileNotFoundError:
#         # 重要的错误处理
#         return "Error: Image file not found at path: " + image_path

# # 启动服务器（使用默认的 stdio 传输方式）
# if __name__ == "__main__":
#     mcp.run()