"""Define the configurable parameters for the agent."""

import os
from dataclasses import dataclass, field, fields
from typing import Literal, Optional

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated

from memory_graph.prompts import SYSTEM_PROMPT


@dataclass(kw_only=True)
class MemoryConfig:
    """Configuration for memory-related operations."""

    name: str
    description: str

    parameters: dict
    """The JSON Schema of the memory document to manage."""
    system_prompt: Optional[str] = SYSTEM_PROMPT
    """The system prompt to use for the memory assistant."""
    update_mode: Literal["patch", "insert"] = field(default="patch")
    """Whether to continuously patch the memory, or treat each new

    generation as a new memory.

    Patching is useful for maintaining a structured profile or core list
    of memories. Inserting is useful for maintaining all interactions and
    not losing any information.

    For patched memories, you can GET the current state at any given time.
    For inserted memories, you can query the full history of interactions.
    """


@dataclass(kw_only=True)
class Configuration:
    """Main configuration class for the memory graph system."""

    user_id: str = "default"
    """The ID of the user to remember in the conversation."""
    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-3-5-sonnet-20240620",
        metadata={
            "description": "The name of the language model to use for the agent. "
            "Should be in the form: provider/model-name."
        },
    )

    """The model to use for generating memories. """
    memory_types: list[MemoryConfig] = field(default_factory=list)
    """The memory_types for the memory assistant."""

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None):
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        values["memory_types"] = [
            MemoryConfig(**v) for v in (values["memory_types"] or [])
        ]
        return cls(**{k: v for k, v in values.items() if v})
