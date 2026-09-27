# Databy AI MCP Server

Self-directed AI Agent.

## Serve Docs

1. Install `mkdocs` with `pip` or `brew` if on mac otherwise refer to google for windows.
2. Run  `mkdocs build` and for more informations run`mkdocs --help` for more info commands/args

## Testing Locally

- Run the server directly:
  - `uv run databy-ai-mcp` (entry point defined in `pyproject.toml`), or
  - `PYTHONPATH=src uv run python -m databy_ai_mcp.server`
- Run the unit tests:
  - `python -m unittest discover -s tests -p "test_*.py"`
- Validate against a real Claude Code client over stdio (recommended over FastMCP's own test client — its `Client` mints a new `ctx.session_id` per tool call, which makes session-scoped state like file uploads look broken when it isn't):
  - Write an `.mcp.json` pointing `command` at the project venv's Python and `args` at `["-m", "databy_ai_mcp.server"]`
  - Run `claude -p "call list_files and report the result" --mcp-config .mcp.json --strict-mcp-config --allowedTools "mcp__<server-name>__<tool-name>"`
  - `--mcp-config` sidesteps `claude mcp add` issues under a restrictive sandbox (blocked write paths, read-only `~/.claude.json`) and the interactive-approval step for project-scoped servers
- Scope: the server only runs over stdio today (`mcp.run()` with no transport arg) — Claude Web/Desktop and HTTP/SSE are not covered by any of the above

## MCP Tools

- Data Profiling:
  - `ydata-profiling` display static `HTML`
    - Agent Interaction:
      - Passes as context caching
    - Agent Tools:
      - `databy_profile`
      - `databy_clean` (Workflow Dependency)

- Statistical Inference
  - PySpark Tools to handle big dataset
  - Agent Tools:
    - `databy_stat_infer`
    - `databy_ab_test`
