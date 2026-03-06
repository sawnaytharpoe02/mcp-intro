"""
OpenRouter provider implementation.

OpenRouter provides free access to multiple AI models through an
OpenAI-compatible API. This is the ONLY file that contains
OpenRouter/OpenAI-specific code.

Free models available on OpenRouter:
  - google/gemini-2.0-flash-exp:free
  - meta-llama/llama-3.3-8b-instruct:free
  - mistralai/mistral-small-3.1-24b-instruct:free
  - deepseek/deepseek-chat-v3-0324:free
  
See full list: https://openrouter.ai/models?q=:free
"""

import json
from typing import Optional
from openai import OpenAI

from core.llm_provider import LLMProvider, LLMMessage, LLMResponse, ToolCall, ToolResult


class OpenRouterProvider(LLMProvider):
    def __init__(self, model: str, api_key: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model

    def chat(
        self,
        messages: list[LLMMessage],
        system: Optional[str] = None,
        temperature: float = 1.0,
        tools: Optional[list] = None,
    ) -> LLMResponse:
        # Convert standardized messages to OpenAI format
        openai_messages = self._convert_messages(messages, system)

        params = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": temperature,
        }

        if tools:
            params["tools"] = tools

        response = self.client.chat.completions.create(**params)
        return self._parse_response(response)

    def format_tools(self, mcp_tools: list[dict]) -> list[dict]:
        """Convert MCP tool format to OpenAI function calling format."""
        if not mcp_tools:
            return []

        openai_tools = []
        for tool in mcp_tools:
            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("input_schema", {}),
                    },
                }
            )
        return openai_tools

    def format_tool_results(self, tool_results: list[ToolResult]) -> LLMMessage:
        """Convert tool results into a standardized message."""
        msg = LLMMessage(role="user", tool_results=tool_results)
        # Store raw OpenAI-format tool result messages
        msg.raw = [
            {
                "role": "tool",
                "tool_call_id": result.tool_call_id,
                "content": result.content,
            }
            for result in tool_results
        ]
        return msg

    def _convert_messages(
        self, messages: list[LLMMessage], system: Optional[str] = None
    ) -> list[dict]:
        """Convert standardized messages to OpenAI format."""
        openai_messages = []

        if system:
            openai_messages.append({"role": "system", "content": system})

        for msg in messages:
            # Tool result messages — expand into individual tool messages
            if msg.tool_results and msg.raw:
                openai_messages.extend(msg.raw)
            elif msg.role == "assistant" and msg.tool_calls:
                # Assistant message with tool calls
                assistant_msg = {
                    "role": "assistant",
                    "content": msg.text or None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments),
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                }
                openai_messages.append(assistant_msg)
            else:
                role = "user" if msg.role == "user" else "assistant"
                openai_messages.append(
                    {"role": role, "content": msg.text or ""}
                )

        return openai_messages

    def _parse_response(self, response) -> LLMResponse:
        """Parse an OpenAI-format response into standardized format."""
        choice = response.choices[0]
        message = choice.message

        text = message.content or ""
        tool_calls = []

        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except (json.JSONDecodeError, TypeError):
                    args = {}

                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=args,
                    )
                )

        return LLMResponse(
            text=text,
            tool_calls=tool_calls,
            raw=response,
        )
