# MoSPI MCP Server

Production-ready MCP (Model Context Protocol) server for accessing MoSPI (Ministry of Statistics and Programme Implementation) data APIs. Built with FastMCP 2.0.

## Features

- **18 MoSPI Datasets**: "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "Energy", "HCES", "NSS78", "TUS", "NFHS", "ASUSE", "Gender", "RBI", "EnvStats", "AISHE", "CPIALRL", "NSS77"
- **FastMCP 2.0**: Modern, simplified, production-ready framework
- **Multiple Deployment Options**: FastMCP Cloud, Docker, or self-hosted
- **HTTP & stdio transports**: Remote access or local MCP clients

## Quick Start

### Local Development

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**

   ```bash
   # Method 1: Direct Python execution
   python mospi_server.py

   # Method 2: Using FastMCP CLI (recommended)
   fastmcp run mospi_server.py:mcp --transport http --port 8000
   ```

3. **Access the Server**
   - Server URL: `http://localhost:8000/mcp`
   - The server runs with HTTP transport for remote access
   - For local stdio access: `fastmcp run mospi_server.py:mcp` (no transport flag)

### Test the Server

```python
import asyncio
from fastmcp import Client

async def test_server():
    async with Client("http://localhost:8000/mcp") as client:
        # Get API documentation
        result = await client.call_tool("know_about_mospi_api", {})
        print(result)

asyncio.run(test_server())
```

## Production Deployment

### Option 1: FastMCP Cloud (Recommended)

[FastMCP Cloud](https://fastmcp.cloud) is **free for personal servers** and optimized for FastMCP deployments.

**Steps:**

1. Push your code to GitHub
2. Sign in to [FastMCP Cloud](https://fastmcp.cloud) with GitHub
3. Create a new project and enter `mospi_server.py:mcp` as the entrypoint
4. Done! Your server is live at `https://your-project.fastmcp.app/mcp`

**Benefits:**

- Zero configuration
- Built-in authentication
- Automatic HTTPS
- Web-based testing interface
- Free for personal use

### Option 2: Docker Deployment

#### Build and Run Locally

```bash
# Build the image
docker build -t mospi-mcp .

# Run the container
docker run -d \
  -p 8000:8000 \
  --name mospi-server \
  mospi-mcp

# Test the server
curl http://localhost:8000/mcp
```

#### Using GitHub Container Registry

The included GitHub Actions workflow automatically builds and publishes Docker images.

**Setup:**

1. Push to GitHub (triggers auto-build)
2. Image published to: `ghcr.io/YOUR_USERNAME/mospi-mcp-deployment:latest`
3. Deploy anywhere:

```bash
docker run -d \
  -p 8000:8000 \
  ghcr.io/YOUR_USERNAME/mospi-mcp-deployment:latest
```

### Option 3: PaaS Deployment (Railway, Render, etc.)

#### Railway

1. Connect your GitHub repository
2. Railway auto-detects the Dockerfile
3. Server deploys automatically on push to `main`

#### Render

1. Create a new Web Service
2. Select "Docker" environment
3. Point to your repository
4. Set health check path to `/health` (FastMCP provides this automatically)

## Architecture

### Components

- **mospi_server.py**: Main FastMCP 2.0 server entry point
- **mospi/**: Dataset modules with 55+ MCP tools (18 datasets × 3 tools each)
- **Dockerfile**: Container definition using FastMCP CLI
- **.github/workflows/deploy.yml**: CI/CD pipeline for auto-builds

## Available Tools

The server provides 55+ MCP tools across 18 datasets. Each dataset has 3 tools:

- `get_X_indicators()`: List available indicators
- `get_X_metadata()`: Get filter codes for an indicator
- `get_X_data()`: Fetch actual data

**Datasets:** PLFS, CPI, IIP, ASI, NAS, WPI, Energy, HCES, NSS78, TUS, NFHS, ASUSE, Gender, RBI, EnvStats, AISHE, CPIALRL, NSS77

**Main tool:** `know_about_mospi_api()` - Complete API documentation (call this first)

## CLI Usage

FastMCP 2.0 includes a powerful CLI:

```bash
# Run with different transports
fastmcp run mospi_server.py:mcp                           # stdio (default)
fastmcp run mospi_server.py:mcp --transport http          # HTTP on port 8000
fastmcp run mospi_server.py:mcp --transport http --port 3000  # Custom port

# Development mode with auto-reload
fastmcp dev mospi_server.py:mcp --transport http

# Get server info
fastmcp inspect mospi_server.py:mcp
```

## Configuration

### Environment Variables

| Variable | Required | Description                    |
| -------- | -------- | ------------------------------ |
| `PORT`   | No       | Port to run on (default: 8000) |

**Note:** FastMCP 2.0 has built-in auth support. For production deployments with authentication, use FastMCP Cloud or configure auth in your FastMCP server initialization.

## Development

### Project Structure

```
mospi-mcp-deployment/
├── mospi_server.py          # Main FastMCP server entry point
├── mospi/                   # Dataset modules
│   ├── __init__.py
│   ├── client.py            # MoSPI API client
│   └── datasets/            # 18 dataset tool modules
├── tests/                   # Test files for all datasets
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container definition
├── README.md                # This file
└── .github/workflows/       # CI/CD pipeline
```

### Testing Locally

```bash
# Install in development mode
pip install -e .

# Run tests (if you add them)
pytest

# Run with auto-reload during development
fastmcp dev mospi_server.py:mcp --transport http
```

## Resources

- **FastMCP Documentation**: https://gofastmcp.com
- **FastMCP Cloud**: https://fastmcp.cloud (free for personal use)
- **Model Context Protocol**: https://modelcontextprotocol.io
- **MoSPI Open APIs**: https://api.mospi.gov.in

## License

This project provides an interface to MoSPI's public APIs. Refer to MoSPI's terms of service for data usage guidelines.

---

**Fun Facts:**

- 🚀 Built with 55+ MCP tools across 18 datasets
- ☕ Powered by lots of coffee and dedication to open data

### Acknowledgments

Special thanks to the **Ministry of Statistics and Programme Implementation (MoSPI)** for providing open APIs and **Bharat Digital** to coordinate the creation of the MCP that makes this data accessible to all.

---
