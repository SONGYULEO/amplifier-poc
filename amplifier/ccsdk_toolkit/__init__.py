"""
Gemini CLI SDK Toolkit

A comprehensive toolkit for building robust applications with the Gemini CLI SDK.
Provides core functionality, configuration management, session persistence,
structured logging, and CLI tool generation.

Quick Start:
    >>> from amplifier.ccsdk_toolkit import GeminiSession, SessionOptions
    >>> async with GeminiSession() as session:
    ...     response = await session.query("Hello!")
    ...     print(response.content)

Modules:
    - core: Core SDK wrapper with error handling
    - config: Configuration management
    - sessions: Session state persistence
    - logger: Structured logging
    - cli: CLI tool builder
"""

# Core functionality
# CLI building
from .cli import CliBuilder
from .cli import CliTemplate

# Configuration management
from .config import AgentConfig
from .config import AgentDefinition
from .config import ConfigLoader
from .config import EnvironmentConfig
from .config import MCPServerConfig
from .config import ToolConfig
from .config import ToolkitConfig
from .config import ToolPermissions
from .core import CCSDKSession
from .core import GeminiSession
from .core import SDKNotAvailableError
from .core import SessionError
from .core import SessionOptions
from .core import SessionResponse
from .core import check_gemini_cli
from .core import query_with_retry
from .logger import LogEvent
from .logger import LogFormat
from .logger import LogLevel
from .logger import ToolkitLogger
from .logger import create_logger

# Session management
from .sessions import SessionManager
from .sessions import SessionMetadata
from .sessions import SessionState

__version__ = "0.1.0"

__all__ = [
    # Core
    "CCSDKSession",
    "GeminiSession",
    "SessionOptions",
    "SessionResponse",
    "SessionError",
    "SDKNotAvailableError",
    "check_gemini_cli",
    "query_with_retry",
    # Config
    "AgentConfig",
    "AgentDefinition",
    "ToolConfig",
    "ToolkitConfig",
    "ToolPermissions",
    "MCPServerConfig",
    "EnvironmentConfig",
    "ConfigLoader",
    # Sessions
    "SessionManager",
    "SessionState",
    "SessionMetadata",
    # Logger
    "ToolkitLogger",
    "create_logger",
    "LogLevel",
    "LogFormat",
    "LogEvent",
    # CLI
    "CliBuilder",
    "CliTemplate",
]
