# Weather MCP Lambda Server

A FastMCP server deployed on AWS Lambda that provides weather information. This project demonstrates how to run an MCP (Model Context Protocol) server as a serverless function using AWS Lambda and API Gateway.

## 📋 Prerequisites

- Python 3.13+
- AWS Account
- AWS CLI configured with credentials
- SAM CLI installed ([Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))
- Claude Desktop app

## 🚀 Running Locally

### 1. Install Dependencies

```bash
cd src
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

The server will start on `http://0.0.0.0:8080`

### 3. Test the Server

You can test the server locally by sending HTTP requests:

```bash
curl -X POST http://localhost:8080/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_weather", "arguments": {"city": "San Francisco"}}'
```

## 🔨 Deploying with SAM CLI

### 1. Build the Application

```bash
sam build
```

This command:
- Packages your Python code and dependencies
- Prepares the CloudFormation template
- Creates a `.aws-sam` build directory

### 2. Deploy to AWS

#### First-time Deployment (Guided)

```bash
sam deploy --guided
```

You'll be prompted for:
- **Stack Name**: Name for your CloudFormation stack (default: `test-mcp`)
- **AWS Region**: Where to deploy (default: `ap-southeast-1`)
- **Profile**: AWS CLI profile to use (default: `lamdalat`)
- **Confirm changes**: Review changes before deployment
- **Capabilities**: Confirm `CAPABILITY_IAM` for IAM resource creation

#### Subsequent Deployments

After the first deployment, simply run:

```bash
sam deploy
```

This uses the configuration saved in `samconfig.toml`.

### 3. Get Your API Endpoint

After deployment completes, you'll see output similar to:

```
Outputs
-------
Key: McpApiUrl
Description: Your FastMCP API Gateway Endpoint URL
Value: https://abc123xyz.execute-api.ap-southeast-1.amazonaws.com/
```

Copy this URL - you'll need it for Claude Desktop configuration.

### 4. Test Your Deployed API

```bash
curl -X POST https://YOUR-API-URL/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_weather", "arguments": {"city": "Paris"}}'
```

## 🤖 Importing into Claude Desktop

### 1. Locate Claude Desktop Config File

The configuration file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 2. Edit the Configuration

Open the config file and add your MCP server:

```json
{
  "mcpServers": {
    "my-aws-lambda-mcp": {
      "command": "/Users/mac/.volta/bin/npx", <-- Adjust path if necessary
      "args": [
        "-y",
        "mcp-remote",
        "YOUR-API-URL" <-- Replace with your API URL
      ]
    }
  }
}
```

Replace `YOUR-API-URL` with the actual API Gateway endpoint from the deployment output.

### 3. Restart Claude Desktop

Completely quit and restart the Claude Desktop application for the changes to take effect.

### 4. Verify Installation

In Claude Desktop, you should now be able to:
- See the weather tool in the available tools
- Ask Claude: "What's the weather in Tokyo?"
- Claude will use your Lambda MCP server to fetch the weather information

## 🧹 Cleanup

To delete all AWS resources:

```bash
sam delete
```

This will remove:
- Lambda function
- API Gateway
- CloudFormation stack
- All associated resources

## 📁 Project Structure

```
.
├── README.md                 # This file
├── template.yaml            # SAM CloudFormation template
├── samconfig.toml           # SAM deployment configuration
└── src/
    ├── main.py              # FastMCP server implementation
    ├── requirements.txt     # Python dependencies
    └── run.sh              # Lambda startup script
```

## 🛠️ How It Works

1. **FastMCP Server**: The `main.py` file defines an MCP server using FastMCP with HTTP transport
2. **Lambda Web Adapter**: Converts API Gateway requests into HTTP requests for FastMCP
3. **API Gateway**: Provides a public HTTPS endpoint for the Lambda function
4. **Claude Desktop**: Connects to the API Gateway endpoint and uses the MCP tools

## 📝 Configuration Details

### SAM Template

The `template.yaml` defines:
- HTTP API Gateway for external access
- Lambda function with Python 3.13 runtime
- AWS Lambda Web Adapter layer (version 25)
- Environment variables for port configuration

### FastMCP Configuration

The server is configured with:
- `stateless_http=True`: Optimizes for serverless environment
- `json_response=True`: Ensures compatibility with API Gateway (no SSE streaming)
- `transport="http"`: Uses HTTP instead of stdio

## 🔧 Customization

### Adding More Tools

Edit `src/main.py` and add more MCP tools:

```python
@mcp.tool()
def another_tool(param: str) -> str:
    """Description of your tool."""
    return f"Result: {param}"
```

After making changes, rebuild and redeploy:

```bash
sam build && sam deploy
```

### Changing AWS Region

Edit `samconfig.toml` and update the `region` parameter, then redeploy.

### Adjusting Lambda Settings

Edit `template.yaml` to modify:
- `MemorySize`: Allocated memory (affects CPU)
- `Timeout`: Maximum execution time
- `Architectures`: Switch between x86_64 and arm64

## 🐛 Troubleshooting

### Local Testing Issues

- Ensure port 8080 is not in use
- Verify Python 3.13+ is installed
- Check all dependencies are installed

### Deployment Issues

- Verify AWS credentials are configured: `aws configure`
- Ensure SAM CLI is up to date: `sam --version`
- Check CloudFormation stack events in AWS Console

### Claude Desktop Connection Issues

- Verify the API URL is correct (include trailing slash)
- Check API Gateway endpoint is accessible
- Restart Claude Desktop after config changes
- Check Claude Desktop logs for connection errors

## 📚 Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [AWS Lambda Web Adapter](https://github.com/awslabs/aws-lambda-web-adapter)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 📄 License

This project is provided as-is for demonstration purposes.
