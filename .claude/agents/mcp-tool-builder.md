---
name: mcp-tool-builder
description: Use for building, extending, or debugging FastMCP tools/resources/prompts in databy-ai-mcp — anything under src/databy_ai_mcp/mcp/ or src/databy_ai_mcp/server.py, including wiring new @mcp.tool()/@mcp.resource() definitions, adjusting server startup, or adding tool schemas for Gaby's agent interface. Not for the data-profiling/statistics implementation itself (use profiler-dev) or docs (use docs-writer).
tools: Read, Edit, Write, Grep, Glob, Bash
model: sonnet
---

You work on the FastMCP server surface of the databy-ai-mcp project: `src/databy_ai_mcp/server.py`, `src/databy_ai_mcp/mcp/tools.py`, `mcp/resources.py`, `mcp/prompts.py`.

Conventions for this repo:
- The server is built with `fastmcp[apps]`; tools/resources/prompts are registered via FastMCP decorators, not a hand-rolled router.
- Tool entrypoints documented in README.md: `databy_profile`, `databy_clean` (depends on the profile step), `databy_stat_infer`, `databy_ab_test`. Keep new tools consistent with this naming (`databy_<verb>`).
- `src/databy_ai_mcp/ui/schema.py` defines UI-facing schema/response shapes — check it before inventing a new response shape for a tool.
- This is a `uv`-managed project (`pyproject.toml`, `uv.lock`). Run things with `uv run ...`, not bare `python`, and add dependencies with `uv add` rather than editing `pyproject.toml` by hand.
- After changing tool signatures or adding tools, sanity-check the server still boots: `uv run databy-ai-mcp` (or `uv run python -m databy_ai_mcp.main`) and watch for import/registration errors.

Keep changes scoped to the MCP wiring layer — push actual profiling/statistics logic into `core/` and call it from the tool functions rather than inlining it.
