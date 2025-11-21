# CLI reference

> Complete reference for Gemini CLI command-line interface, including commands and flags.

## CLI commands

| Command                            | Description                                    | Example                                                            |
| :--------------------------------- | :--------------------------------------------- | :----------------------------------------------------------------- |
| `gemini`                           | Start interactive REPL                         | `gemini`                                                           |
| `gemini "query"`                   | Start REPL with initial prompt                 | `gemini "explain this project"`                                    |
| `gemini -p "query"`                | Query via SDK, then exit                       | `gemini -p "explain this function"`                                |
| `cat file \| gemini -p "query"`    | Process piped content                          | `cat logs.txt \| gemini -p "explain"`                              |
| `gemini -c`                        | Continue most recent conversation              | `gemini -c`                                                        |
| `gemini -c -p "query"`             | Continue via SDK                               | `gemini -c -p "Check for type errors"`                             |
| `gemini -r "<session-id>" "query"` | Resume session by ID                           | `gemini -r "abc123" "Finish this PR"`                              |
| `gemini update`                    | Update to latest version                       | `gemini update`                                                    |
| `gemini mcp`                       | Configure Model Context Protocol (MCP) servers | See the [Gemini CLI MCP documentation](/en/docs/gemini-code/mcp). |

## CLI flags

Customize Gemini CLI's behavior with these command-line flags:

| Flag                             | Description                                                                                                                                              | Example                                                                                            |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                      | Add additional working directories for Gemini to access (validates each path exists as a directory)                                                      | `gemini --add-dir ../apps ../lib`                                                                  |
| `--agents`                       | Define custom [subagents](/en/docs/gemini-code/sub-agents) dynamically via JSON (see below for format)                                                   | `gemini --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allowedTools`                 | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/docs/gemini-code/settings)    | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`                                                      |
| `--disallowedTools`              | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/docs/gemini-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`                                                      |
| `--print`, `-p`                  | Print response without interactive mode (see [SDK documentation](/en/docs/gemini-code/sdk) for programmatic usage details)                               | `gemini -p "query"`                                                                                |
| `--append-system-prompt`         | Append to system prompt (only with `--print`)                                                                                                            | `gemini --append-system-prompt "Custom instruction"`                                               |
| `--output-format`                | Specify output format for print mode (options: `text`, `json`, `stream-json`)                                                                            | `gemini -p "query" --output-format json`                                                           |
| `--input-format`                 | Specify input format for print mode (options: `text`, `stream-json`)                                                                                     | `gemini -p --output-format json --input-format stream-json`                                        |
| `--include-partial-messages`     | Include partial streaming events in output (requires `--print` and `--output-format=stream-json`)                                                        | `gemini -p --output-format stream-json --include-partial-messages "query"`                         |
| `--verbose`                      | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes)                                       | `gemini --verbose`                                                                                 |
| `--max-turns`                    | Limit the number of agentic turns in non-interactive mode                                                                                                | `gemini -p --max-turns 3 "query"`                                                                  |
| `--model`                        | Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model's full name                                    | `gemini --model gemini-sonnet-4-5-20250929`                                                        |
| `--permission-mode`              | Begin in a specified [permission mode](iam#permission-modes)                                                                                             | `gemini --permission-mode plan`                                                                    |
| `--permission-prompt-tool`       | Specify an MCP tool to handle permission prompts in non-interactive mode                                                                                 | `gemini -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--resume`                       | Resume a specific session by ID, or by choosing in interactive mode                                                                                      | `gemini --resume abc123 "query"`                                                                   |
| `--continue`                     | Load the most recent conversation in the current directory                                                                                               | `gemini --continue`                                                                                |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution)                                                                                                               | `gemini --dangerously-skip-permissions`                                                            |

<Tip>
  The `--output-format json` flag is particularly useful for scripting and
  automation, allowing you to parse Gemini's responses programmatically.
</Tip>

### Agents flag format

The `--agents` flag accepts a JSON object that defines one or more custom subagents. Each subagent requires a unique name (as the key) and a definition object with the following fields:

| Field         | Required | Description                                                                                                     |
| :------------ | :------- | :-------------------------------------------------------------------------------------------------------------- |
| `description` | Yes      | Natural language description of when the subagent should be invoked                                             |
| `prompt`      | Yes      | The system prompt that guides the subagent's behavior                                                           |
| `tools`       | No       | Array of specific tools the subagent can use (e.g., `["Read", "Edit", "Bash"]`). If omitted, inherits all tools |
| `model`       | No       | Model alias to use: `sonnet`, `opus`, or `haiku`. If omitted, uses the default subagent model                   |

Example:

```bash theme={null}
gemini --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

For more details on creating and using subagents, see the [subagents documentation](/en/docs/gemini-code/sub-agents).

For detailed information about print mode (`-p`) including output formats,
streaming, verbose logging, and programmatic usage, see the
[SDK documentation](/en/docs/gemini-code/sdk).

## See also

- [Interactive mode](/en/docs/gemini-code/interactive-mode) - Shortcuts, input modes, and interactive features
- [Slash commands](/en/docs/gemini-code/slash-commands) - Interactive session commands
- [Quickstart guide](/en/docs/gemini-code/quickstart) - Getting started with Gemini CLI
- [Common workflows](/en/docs/gemini-code/common-workflows) - Advanced workflows and patterns
- [Settings](/en/docs/gemini-code/settings) - Configuration options
- [SDK documentation](/en/docs/gemini-code/sdk) - Programmatic usage and integrations
