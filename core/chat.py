from core.llm_provider import LLMProvider, LLMMessage
from mcp_client import MCPClient
from core.tools import ToolManager


class Chat:
    def __init__(self, llm: LLMProvider, clients: dict[str, MCPClient]):
        self.llm: LLMProvider = llm
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[LLMMessage] = []

    async def _process_query(self, query: str):
        self.messages.append(LLMMessage(role="user", text=query))

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        # Get MCP tools (provider-agnostic format)
        mcp_tools = await ToolManager.get_all_mcp_tools(self.clients)
        # Let the provider convert them to its own format
        formatted_tools = self.llm.format_tools(mcp_tools)

        while True:
            response = self.llm.chat(
                messages=self.messages,
                tools=formatted_tools if formatted_tools else None,
            )

            # Store assistant response
            self.messages.append(
                LLMMessage(
                    role="assistant",
                    text=response.text,
                    tool_calls=response.tool_calls,
                    raw=response.raw,
                )
            )

            if response.has_tool_calls:
                if response.text:
                    print(response.text)

                # Execute tools (provider-agnostic)
                tool_results = await ToolManager.execute_tool_calls(
                    self.clients, response
                )

                # Let provider format tool results into a message
                tool_msg = self.llm.format_tool_results(tool_results)
                self.messages.append(tool_msg)
            else:
                final_text_response = response.text
                break

        return final_text_response
