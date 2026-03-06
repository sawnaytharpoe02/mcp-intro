"""
LLM Provider abstraction layer.

This module defines a standard interface for LLM providers so that
swapping between models (Claude, Gemini, OpenAI, etc.) only requires
changing ONE file — the concrete provider implementation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class LLMMessage:
    """A standardized message in the conversation history."""

    role: str  # "user" or "assistant"
    text: str = ""
    tool_calls: list["ToolCall"] = field(default_factory=list)
    tool_results: list["ToolResult"] = field(default_factory=list)
    raw: Any = None  # Store the raw provider-specific response if needed


@dataclass
class ToolCall:
    """A standardized tool/function call."""

    id: str
    name: str
    arguments: dict = field(default_factory=dict)


@dataclass
class ToolResult:
    """A standardized tool/function result."""

    tool_call_id: str
    name: str
    content: str = ""
    is_error: bool = False


@dataclass
class LLMResponse:
    """A standardized response from the LLM."""

    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw: Any = None  # The raw provider-specific response object

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0


class LLMProvider(ABC):
    """Abstract base class for LLM providers.

    To add a new provider (e.g., OpenAI, Ollama), just:
    1. Create a new file like `core/providers/openai_provider.py`
    2. Implement this interface
    3. Update .env and main.py to use the new provider

    No other files need to change!
    """

    @abstractmethod
    def chat(
        self,
        messages: list[LLMMessage],
        system: Optional[str] = None,
        temperature: float = 1.0,
        tools: Optional[list[dict]] = None,
    ) -> LLMResponse:
        """Send a chat request and return a standardized response."""
        ...

    @abstractmethod
    def format_tools(self, mcp_tools: list[dict]) -> list[dict]:
        """Convert MCP tool schemas to the provider's tool format.

        Args:
            mcp_tools: List of tools in MCP format:
                [{"name": "...", "description": "...", "input_schema": {...}}, ...]

        Returns:
            Tools formatted for this specific provider's API.
        """
        ...

    @abstractmethod
    def format_tool_results(
        self, tool_results: list[ToolResult]
    ) -> LLMMessage:
        """Convert tool results into a message the provider can understand."""
        ...
