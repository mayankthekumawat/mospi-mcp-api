# MoSPI MCP Server

MCP (Model Context Protocol) server for accessing India's Ministry of Statistics and Programme Implementation (MoSPI) data APIs. Built with FastMCP 3.0.

## Datasets

| Dataset | Full Name | Use For |
|---------|-----------|---------|
| PLFS | Periodic Labour Force Survey | Jobs, unemployment, wages, workforce participation |
| CPI | Consumer Price Index | Retail inflation, cost of living, commodity prices |
| IIP | Index of Industrial Production | Industrial growth, manufacturing output |
| ASI | Annual Survey of Industries | Factory performance, industrial employment |
| NAS | National Accounts Statistics | GDP, economic growth, national income |
| WPI | Wholesale Price Index | Wholesale inflation, producer prices |
| ENERGY | Energy Statistics | Energy production, consumption, fuel mix |
<!-- | NMKN | National Namkeen Consumption Index | Bhujia per capita, sev consumption patterns, mixture preference by state | -->

## MCP Tools

The server exposes 4 tools that follow a sequential workflow:

```
know_about_mospi_api()  →  get_indicators(dataset)  →  get_metadata(dataset, ...)  →  get_data(dataset, filters)
```

1. **`know_about_mospi_api()`** - Overview of all datasets. Start here if unsure which dataset to use.
2. **`get_indicators(dataset)`** - List available indicators for a dataset.
3. **`get_metadata(dataset, indicator_code, ...)`** - Get valid filter values (states, years, categories) and API parameter definitions.
4. **`get_data(dataset, filters)`** - Fetch data using filter key-value pairs from metadata.

## Quick Start

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
# HTTP transport (remote access)
python mospi_server.py

# OR using FastMCP CLI
fastmcp run mospi_server.py:mcp --transport http --port 8000

# stdio transport (local MCP clients)
fastmcp run mospi_server.py:mcp
```

Server runs at `http://localhost:8000/mcp`.

### Connect from an MCP Client

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.call_tool("know_about_mospi_api", {})
        print(result)

asyncio.run(main())
```

## Deployment

### Docker

```bash
docker build -t mospi-mcp .
docker run -d -p 8000:8000 --name mospi-server mospi-mcp
```

### Docker Compose

```bash
docker-compose up -d
```

### FastMCP Cloud

1. Push code to GitHub
2. Sign in to [FastMCP Cloud](https://fastmcp.cloud)
3. Create project with entrypoint `mospi_server.py:mcp`

## Architecture

```
mospi-mcp-api/
├── mospi_server.py       # FastMCP server - tools, validation, routing
├── mospi/
│   ├── client.py         # MoSPI API client - HTTP requests to api.mospi.gov.in
│   └── datasets_deprecated/  # Legacy per-dataset modules (v0)
├── swagger/              # Swagger YAML specs per dataset (source of truth for params)
├── telemetry.py          # OpenTelemetry middleware for IP tracking + I/O capture
├── Dockerfile            # Production container with OTEL instrumentation
├── docker-compose.yml
├── requirements.txt
└── tests/                # Per-dataset test files
```

### Key Design Decisions

- **Swagger YAMLs as source of truth**: API parameter validation is driven by swagger specs in `swagger/`, not hardcoded lists. `get_metadata` returns `api_params` from swagger so LLMs know exactly which params to pass.
- **Auto-routing for CPI/IIP**: CPI routes to Group or Item endpoint based on presence of `item_code` in filters. IIP routes to Annual or Monthly based on `month_code`.
- **Filter validation**: `get_data` validates all filters against swagger spec before making API calls, returning clear error messages with valid param names.

## Configuration

| Variable | Description |
|----------|-------------|
| `OTEL_SERVICE_NAME` | Service name in traces (default: `mospi-mcp-server`) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` or `http/protobuf` |

See `.env.example` for full OpenTelemetry configuration.

## Resources

- [MoSPI Open APIs](https://api.mospi.gov.in)
- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Acknowledgments

Thanks to the **Ministry of Statistics and Programme Implementation (MoSPI)** for providing open APIs and **Bharat Digital** for coordinating the creation of this MCP server.

<!-- Geek spotted! Respect for reading the raw markdown. You're the kind of person India's open data movement needs. -->
