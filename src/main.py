import os
from fastmcp import FastMCP

# 1. Initialize FastMCP tailored for Lambda + API Gateway
# stateless_http=True: Optimizes for serverless (no long-lived connections)
# json_response=True: Bypasses SSE streaming for standard API Gateway compatibility
mcp = FastMCP(
    "Lambda-MCP-Server", 
    stateless_http=True, 
    json_response=True
)

# 2. Define your tools
@mcp.tool()
def get_weather(city: str) -> str:
    """Return the current weather for a given city."""
    return f"The weather in {city} is sunny and 72°F."

# 3. Start the server
def main():
    # The Lambda Web Adapter injects the PORT environment variable (default 8080)
    port = int(os.environ.get("PORT", "8080"))
    
    # Run using the HTTP transport
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port
    )

if __name__ == "__main__":
    main()