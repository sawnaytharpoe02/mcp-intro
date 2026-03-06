import json
from typing import Optional, List
from mcp.types import CallToolResult, TextContent
from mcp_client import MCPClient
from core.llm_provider import LLMResponse, ToolResult


class ToolManager:
    @classmethod
    async def get_all_mcp_tools(cls, clients: dict[str, MCPClient]) -> list[dict]:
        """Gets all tools from MCP clients in a standardized format.

        Returns a list of dicts with: name, description, input_schema
        The LLM provider will then convert this to its own format.
        """
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    async def execute_tool_calls(
        cls, clients: dict[str, MCPClient], response: LLMResponse
    ) -> list[ToolResult]:
        """Execute tool calls from an LLM response and return standardized results."""
        results: list[ToolResult] = []

        for tool_call in response.tool_calls:
            tool_name = tool_call.name
            tool_input = tool_call.arguments

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                results.append(
                    ToolResult(
                        tool_call_id=tool_call.id,
                        name=tool_name,
                        content="Could not find that tool",
                        is_error=True,
                    )
                )
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)

                results.append(
                    ToolResult(
                        tool_call_id=tool_call.id,
                        name=tool_name,
                        content=content_json,
                        is_error=bool(tool_output and tool_output.isError),
                    )
                )
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                results.append(
                    ToolResult(
                        tool_call_id=tool_call.id,
                        name=tool_name,
                        content=json.dumps({"error": error_message}),
                        is_error=True,
                    )
                )

        return results
