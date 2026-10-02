# Simple Hedge Fund

This project is a stripped-down rewrite of the larger `ai-hedge-fund-main` codebase. It is built for learning, not trading. The goal is to show how a small agent system can be structured with:

- a CLI entrypoint
- a normalized data layer
- two focused analyst agents
- a pluggable LLM provider seam
- a simple orchestrator that combines agent outputs

There is no UI, no backtesting engine, and no test suite.

## What it does

For each ticker:

1. Fetches a small market snapshot from `yfinance`
2. Runs a simplified Warren Buffett agent
3. Runs a simplified Peter Lynch agent
4. Combines their signals into one final recommendation
5. Prints the result in the terminal

The agents can work in two modes:

- heuristic-only mode: deterministic rules, no API key required
- LangChain mode: uses an OpenAI chat model to turn the same metrics into a structured agent response

## Project layout

```text
simple-hedge-fund/
├── pyproject.toml
├── README.md
├── .env.example
├── config.example.toml
└── src/simple_hedge_fund/
	├── cli.py
	├── config.py
	├── models.py
	├── orchestrator.py
	├── output.py
	├── agents/
	│   ├── peter_lynch.py
	│   └── warren_buffett.py
	├── data/
	│   └── yfinance_service.py
	└── llm/
		├── base.py
		├── factory.py
		└── openai_provider.py
```

## Install with uv

```bash
uv sync
```

## Configuration

Copy `.env.example` to `.env` if you want OpenAI support.

```bash
cp .env.example .env
```

You can also start from the example config file:

```bash
cp config.example.toml config.toml
```

Example `config.toml`:

```toml
provider = "openai"
model = "gpt-4.1-mini"
use_llm = true
temperature = 0.1
reasoning = true
default_tickers = ["AAPL", "MSFT"]
```

If `OPENAI_API_KEY` is missing, the app automatically falls back to heuristic-only mode.

## Run

Use the config file defaults:

```bash
uv run simple-hedge-fund
```

Pass tickers directly:

```bash
uv run simple-hedge-fund AAPL MSFT
```

Disable LLM calls explicitly:

```bash
uv run simple-hedge-fund AAPL --no-llm
```

Override provider or model from the command line:

```bash
uv run simple-hedge-fund NVDA --provider openai --model gpt-4.1-mini
```

## How LangChain fits in

This project keeps LangChain in one narrow place: the LLM provider layer. Each agent:

1. gathers normalized inputs from the data service
2. computes a simple heuristic baseline
3. optionally asks a LangChain-backed model for a structured response
4. falls back to the heuristic response if no provider is configured

That gives you a small example of the common agent pattern without needing LangGraph or a large workflow engine.

## How this differs from the original repo

Compared with `ai-hedge-fund-main`, this version intentionally removes:

- LangGraph workflow orchestration
- many analyst personas
- risk and portfolio manager agents
- FastAPI, database, frontend, and Docker setup
- backtesting and performance reporting

What remains is the smallest useful slice for learning the structure.

