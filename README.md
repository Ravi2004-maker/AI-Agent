# AI-Agent

Production-ready skeleton for a Playwright-based browser automation agent. This repository
provides a minimal, deterministic runtime and test suite that can grow with a larger
codebase while keeping configuration centralized and explicit.

## Quickstart

```bash
python -m src.main https://example.com
```

## Configuration

Configuration can be set via CLI flags or environment variables. CLI flags override
environment variables. See `src/agent/config.py` for defaults.

### CLI flags

```bash
python -m src.main https://example.com \
  --headless \
  --default-timeout-ms 30000 \
  --navigation-timeout-ms 30000 \
  --user-agent "AI-Agent/1.0" \
  --viewport 1280x720
```

### Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `AI_AGENT_HEADLESS` | `true`/`false` toggle for headless mode | `true` |
| `AI_AGENT_DEFAULT_TIMEOUT_MS` | Default timeout for Playwright actions | `30000` |
| `AI_AGENT_NAVIGATION_TIMEOUT_MS` | Timeout for page navigation | `30000` |
| `AI_AGENT_USER_AGENT` | Custom user agent string | unset |
| `AI_AGENT_VIEWPORT` | Viewport in `WIDTHxHEIGHT` format | unset |

## Architecture

- `src/agent/config.py` owns configuration parsing and validation.
- `src/agent/browser.py` owns Playwright lifecycle, context defaults, and navigation.
- `src/agent/core.py` coordinates the agent runtime and validates inputs.
- `src/main.py` provides CLI entrypoint that references this README for usage.

## Testing

```bash
pytest -q
```

Tests use deterministic fakes to avoid external network dependency.
