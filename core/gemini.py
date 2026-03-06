"""
Google Gemini provider implementation.

This is the ONLY file you need to change to swap to a different AI model.
"""

from typing import Optional
from google import genai
from google.genai import types as genai_types

from core.llm_provider import LLMProvider, LLMMessage, LLMResponse, ToolCall, ToolResult


class GeminiProvider(LLMProvider):
    def __init__(self, model: str, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def chat(
        self,
        messages: list[LLMMessage],
        system: Optional[str] = None,
        temperature: float = 1.0,
        tools: Optional[list] = None,
    ) -> LLMResponse:
        # Convert standardized messages to Gemini format
        gemini_messages = self._convert_messages(messages)

        config_params = {"temperature": temperature}

        if system:
            config_params["system_instruction"] = system

        if tools:
            config_params["tools"] = tools

        config = genai_types.GenerateContentConfig(**config_params)

        response = self.client.models.generate_content(
            model=self.model,
            contents=gemini_messages,
            config=config,
        )

        return self._parse_response(response)

    def format_tools(self, mcp_tools: list[dict]) -> list:
        """Convert MCP tool format to Gemini function declarations."""
        if not mcp_tools:
            return []

        func_declarations = []
        for tool in mcp_tools:
            func_decl = genai_types.FunctionDeclaration(
                name=tool["name"],
                description=tool.get("description", ""),
                parameters=_convert_schema(tool.get("input_schema"))
                if tool.get("input_schema")
                else None,
            )
            func_declarations.append(func_decl)

        return [genai_types.Tool(function_declarations=func_declarations)]

    def format_tool_results(self, tool_results: list[ToolResult]) -> LLMMessage:
        """Convert tool results into a standardized message with Gemini-specific raw data."""
        parts = []
        for result in tool_results:
            parts.append(
                genai_types.Part.from_function_response(
                    name=result.name,
                    response={
                        "result": result.content,
                        "is_error": result.is_error,
                    },
                )
            )

        msg = LLMMessage(role="user", tool_results=tool_results)
        msg.raw = parts  # Store Gemini-specific format for sending
        return msg

    def _convert_messages(self, messages: list[LLMMessage]) -> list[dict]:
        """Convert standardized messages to Gemini format."""
        gemini_messages = []

        for msg in messages:
            role = "user" if msg.role == "user" else "model"

            # If the message has raw Gemini parts (e.g. tool results), use them
            if msg.raw is not None and msg.tool_results:
                gemini_messages.append({"role": role, "parts": msg.raw})
            elif msg.tool_calls:
                # Reconstruct function_call parts
                parts = []
                if msg.text:
                    parts.append({"text": msg.text})
                for tc in msg.tool_calls:
                    parts.append(
                        {
                            "function_call": {
                                "name": tc.name,
                                "args": tc.arguments,
                            }
                        }
                    )
                gemini_messages.append({"role": role, "parts": parts})
            else:
                gemini_messages.append(
                    {"role": role, "parts": [{"text": msg.text}]}
                )

        return gemini_messages

    def _parse_response(
        self, response: genai_types.GenerateContentResponse
    ) -> LLMResponse:
        """Parse a Gemini response into standardized format."""
        texts = []
        tool_calls = []

        for candidate in response.candidates:
            for i, part in enumerate(candidate.content.parts):
                if part.text:
                    texts.append(part.text)
                elif part.function_call:
                    tool_calls.append(
                        ToolCall(
                            id=f"call_{part.function_call.name}_{i}",
                            name=part.function_call.name,
                            arguments=dict(part.function_call.args)
                            if part.function_call.args
                            else {},
                        )
                    )

        return LLMResponse(
            text="\n".join(texts),
            tool_calls=tool_calls,
            raw=response,
        )


def _convert_schema(schema: dict) -> dict:
    """Convert JSON Schema to Gemini-compatible schema."""
    if not schema:
        return schema

    cleaned = {}

    if "type" in schema:
        cleaned["type"] = schema["type"].upper()
    if "description" in schema:
        cleaned["description"] = schema["description"]
    if "properties" in schema:
        cleaned["properties"] = {
            k: _convert_schema(v) for k, v in schema["properties"].items()
        }
    if "required" in schema:
        cleaned["required"] = schema["required"]
    if "items" in schema:
        cleaned["items"] = _convert_schema(schema["items"])
    if "enum" in schema:
        cleaned["enum"] = schema["enum"]

    return cleaned
