# Overview

> Build custom AI agents with the Gemini CLI SDK

## SDK Options

The Gemini CLI SDK is available in multiple forms to suit different use cases:

- **[Headless Mode](/en/docs/gemini-code/sdk/sdk-headless)** - For CLI scripts and automation
- **[TypeScript SDK](/en/docs/gemini-code/sdk/sdk-typescript)** - For Node.js and web applications
- **[Python SDK](/en/docs/gemini-code/sdk/sdk-python)** - For Python applications and data science
- **[Streaming vs Single Mode](/en/docs/gemini-code/sdk/streaming-vs-single-mode)** - Understanding input modes and best practices

## Why use the Gemini CLI SDK?

Built on top of the agent harness that powers Gemini CLI, the Gemini CLI SDK provides all the building blocks you need to build production-ready agents.

Taking advantage of the work we've done on Gemini CLI including:

- **Context Management**: Automatic compaction and context management to ensure your agent doesn't run out of context.
- **Rich tool ecosystem**: File operations, code execution, web search, and MCP extensibility
- **Advanced permissions**: Fine-grained control over agent capabilities
- **Production essentials**: Built-in error handling, session management, and monitoring
- **Optimized Gemini integration**: Automatic prompt caching and performance optimizations

## What can you build with the SDK?

Here are some example agent types you can create:

**Coding agents:**

- SRE agents that diagnose and fix production issues
- Security review bots that audit code for vulnerabilities
- Oncall engineering assistants that triage incidents
- Code review agents that enforce style and best practices

**Business agents:**

- Legal assistants that review contracts and compliance
- Finance advisors that analyze reports and forecasts
- Customer support agents that resolve technical issues
- Content creation assistants for marketing teams

## Core Concepts

### Authentication

For basic authentication, retrieve an Anthropic API key from the [Anthropic Console](https://console.anthropic.com/) and set the `ANTHROPIC_API_KEY` environment variable.

The SDK also supports authentication via third-party API providers:

- **Amazon Bedrock**: Set `GEMINI_CODE_USE_BEDROCK=1` environment variable and configure AWS credentials
- **Google Vertex AI**: Set `GEMINI_CODE_USE_VERTEX=1` environment variable and configure Google Cloud credentials

For detailed configuration instructions for third-party providers, see the [Amazon Bedrock](/en/docs/gemini-code/amazon-bedrock) and [Google Vertex AI](/en/docs/gemini-code/google-vertex-ai) documentation.

### Full Gemini CLI Feature Support

The SDK provides access to all the default features available in Gemini CLI, leveraging the same file system-based configuration:

- **Subagents**: Launch specialized agents stored as Markdown files in `./.gemini/agents/`
- **Hooks**: Execute custom commands configured in `./.gemini/settings.json` that respond to tool events
- **Slash Commands**: Use custom commands defined as Markdown files in `./.gemini/commands/`
- **Memory (GEMINI.md)**: Maintain project context through `GEMINI.md` files that provide persistent instructions and context

These features work identically to their Gemini CLI counterparts by reading from the same file system locations.

### System Prompts

System prompts define your agent's role, expertise, and behavior. This is where you specify what kind of agent you're building.

### Tool Permissions

Control which tools your agent can use with fine-grained permissions:

- `allowedTools` - Explicitly allow specific tools
- `disallowedTools` - Block specific tools
- `permissionMode` - Set overall permission strategy

### Model Context Protocol (MCP)

Extend your agents with custom tools and integrations through MCP servers. This allows you to connect to databases, APIs, and other external services.

## Related Resources

- [CLI Reference](/en/docs/gemini-code/cli-reference) - Complete CLI documentation
- [GitHub Actions Integration](/en/docs/gemini-code/github-actions) - Automate your GitHub workflow
- [MCP Documentation](/en/docs/gemini-code/mcp) - Extend Gemini with custom tools
- [Common Workflows](/en/docs/gemini-code/common-workflows) - Step-by-step guides
- [Troubleshooting](/en/docs/gemini-code/troubleshooting) - Common issues and solutions
