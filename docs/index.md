# Databy AI MCP Server

Data engineering capabilities as a Claude MCP connector, served on [FastMCP](https://gofastmcp.com).

Databy AI MCP exposes the tabular/text/log data lifecycle — **explore, wrangle, analyze, report** — as tools an LLM can call directly from a Claude session: upload a dataset, profile it, clean it, and get back a summary, with as little manual wrangling as possible.

<div class="dino-grid">
  <div class="dino-card">
    <img src="dinos/dino_matrix.png" alt="Explore">
    <span class="dino-step">Step 1</span>
    <strong>Explore</strong>
    <span class="dino-desc">Upload a dataset and inspect its shape, schema, and session metadata.</span>
  </div>
  <div class="dino-card">
    <img src="dinos/dino_clean.png" alt="Wrangle">
    <span class="dino-step">Step 2</span>
    <strong>Wrangle</strong>
    <span class="dino-desc">Clean and reshape the data based on how messy it is.</span>
  </div>
  <div class="dino-card">
    <img src="dinos/dino_chart.png" alt="Analyze">
    <span class="dino-step">Step 3</span>
    <strong>Analyze</strong>
    <span class="dino-desc">Profile correlations, missing values, and distributions with ydata-profiling.</span>
  </div>
  <div class="dino-card">
    <img src="dinos/dino_tail.png" alt="Report">
    <span class="dino-step">Step 4</span>
    <strong>Report</strong>
    <span class="dino-desc">Hand back a summary, then loop to the next session.</span>
  </div>
</div>

## Getting started

See the [Setup guide](docs/posts/01_setup.md) for installing dependencies with `uv` and running the server.

## What's next

Track in-progress work on the [Roadmap](docs/todos/2808.md).
