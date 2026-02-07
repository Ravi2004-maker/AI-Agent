import argparse
import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.core import Agent
from src.agent.config import AgentConfig, parse_viewport
from src.utils.logger import setup_logger

logger = setup_logger("main")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "AI-Agent browser runner. See README.md for full configuration details."
        )
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://example.com",
        help="URL to visit (default: https://example.com).",
    )
    headless_group = parser.add_mutually_exclusive_group()
    headless_group.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default).",
    )
    headless_group.add_argument(
        "--headed",
        action="store_true",
        help="Run browser with visible UI.",
    )
    parser.add_argument(
        "--default-timeout-ms",
        type=int,
        help="Default timeout for Playwright actions.",
    )
    parser.add_argument(
        "--navigation-timeout-ms",
        type=int,
        help="Timeout for navigation actions.",
    )
    parser.add_argument("--user-agent", type=str, help="Custom user agent string.")
    parser.add_argument(
        "--viewport",
        type=str,
        help="Viewport in WIDTHxHEIGHT format (e.g. 1280x720).",
    )
    return parser


def resolve_config(args: argparse.Namespace) -> AgentConfig:
    env_config = AgentConfig.from_env()
    headless = env_config.headless
    if args.headed:
        headless = False
    elif args.headless:
        headless = True
    default_timeout_ms = args.default_timeout_ms or env_config.default_timeout_ms
    navigation_timeout_ms = (
        args.navigation_timeout_ms or env_config.navigation_timeout_ms
    )
    user_agent = args.user_agent or env_config.user_agent
    viewport = env_config.viewport
    if args.viewport:
        viewport = parse_viewport(args.viewport)
    return AgentConfig(
        headless=headless,
        default_timeout_ms=default_timeout_ms,
        navigation_timeout_ms=navigation_timeout_ms,
        user_agent=user_agent,
        viewport=viewport,
    )


def main():
    logger.info("Agent starting...")
    parser = build_parser()
    args = parser.parse_args()
    config = resolve_config(args)
    agent = Agent(config=config)
    try:
        title = agent.run(args.url)
        logger.info(f"Successfully visited {args.url}. Title: {title}")
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
