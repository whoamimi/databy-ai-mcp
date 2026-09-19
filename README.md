# Databy AI MCP Server

Self-directed AI Agent.

## Serve Docs

1. Install `mkdocs` with `pip` or `brew` if on mac otherwise refer to google for windows.
2. Run  `mkdocs build` and for more informations run`mkdocs --help` for more info commands/args

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
