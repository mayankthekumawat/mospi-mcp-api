"""
Telemetry middleware for MoSPI MCP Server.

Uses FastMCP's native middleware system to capture:
- Client IP address (from X-Forwarded-For or direct connection)
- User-Agent header
- Tool inputs and outputs

All data is added to OpenTelemetry spans for visibility in Jaeger.
"""

import json
from typing import Any

from fastmcp.server.middleware import Middleware, MiddlewareContext
from opentelemetry import trace

# Constants
MAX_ATTRIBUTE_SIZE = 4096  # 4KB limit for span attributes


def truncate_json(value: Any, max_size: int = MAX_ATTRIBUTE_SIZE) -> tuple[str, int]:
    """
    Serialize value to JSON and truncate if necessary.

    Returns:
        Tuple of (truncated_string, original_size_bytes)
    """
    try:
        serialized = json.dumps(value, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        serialized = str(value)

    original_size = len(serialized.encode('utf-8'))

    if original_size > max_size:
        truncated = serialized[:max_size - 50] + f"... [truncated, full size: {original_size} bytes]"
        return truncated, original_size

    return serialized, original_size


def extract_client_ip(headers: dict) -> str:
    """
    Extract client IP from headers, checking proxy headers first.

    Priority: X-Forwarded-For -> X-Real-IP -> unknown
    """
    # X-Forwarded-For may contain multiple IPs: "client, proxy1, proxy2"
    x_forwarded_for = headers.get("x-forwarded-for", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    x_real_ip = headers.get("x-real-ip", "")
    if x_real_ip:
        return x_real_ip.strip()

    return "unknown"


class TelemetryMiddleware(Middleware):
    """
    FastMCP middleware that captures telemetry data in OpenTelemetry spans.

    Captures:
    - client.ip: Client IP address
    - client.user_agent: User-Agent header
    - tool.name: Name of the tool being called
    - tool.input: JSON-serialized input arguments (truncated to 4KB)
    - tool.output: JSON-serialized return value (truncated to 4KB)
    - tool.output_size: Original size of output in bytes
    """

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """Hook that intercepts all tool calls."""
        span = trace.get_current_span()

        # Extract tool info from the MCP message
        # FastMCP uses context.message.name and context.message.arguments directly
        tool_name = getattr(context.message, 'name', None)
        tool_args = getattr(context.message, 'arguments', None)

        # Add pre-execution attributes to span
        if span and span.is_recording():
            if tool_name:
                span.set_attribute("tool.name", tool_name)

            if tool_args is not None:
                input_str, _ = truncate_json(tool_args)
                span.set_attribute("tool.input", input_str)

            # Extract client info from request context
            self._add_client_info_to_span(context, span)

        # Execute the tool
        result = await call_next(context)

        # Add post-execution attributes
        # FastMCP returns result with structured_content attribute
        if span and span.is_recording():
            output_data = getattr(result, 'structured_content', result)
            if output_data is not None:
                output_str, output_size = truncate_json(output_data)
                span.set_attribute("tool.output", output_str)
                span.set_attribute("tool.output_size", output_size)

        return result

    def _add_client_info_to_span(self, context: MiddlewareContext, span) -> None:
        """Extract and add client IP and User-Agent to the span."""
        try:
            # Access FastMCP's request context for HTTP headers
            fastmcp_ctx = context.fastmcp_context
            if not fastmcp_ctx:
                return

            request_ctx = getattr(fastmcp_ctx, 'request_context', None)
            if not request_ctx:
                return

            # Get headers - may be a dict or Headers object
            headers = getattr(request_ctx, 'headers', None)
            if headers is None:
                return

            # Convert to dict if needed (Starlette Headers object)
            if hasattr(headers, 'items'):
                headers_dict = {k.lower(): v for k, v in headers.items()}
            elif isinstance(headers, dict):
                headers_dict = {k.lower(): v for k, v in headers.items()}
            else:
                return

            # Extract and set client IP
            client_ip = extract_client_ip(headers_dict)
            span.set_attribute("client.ip", client_ip)

            # Extract and set User-Agent
            user_agent = headers_dict.get("user-agent", "unknown")
            span.set_attribute("client.user_agent", user_agent)

        except Exception:
            # Don't let telemetry errors break the request
            pass
