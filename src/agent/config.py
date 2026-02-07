from dataclasses import dataclass
import os
from typing import Optional, Tuple


@dataclass(frozen=True)
class AgentConfig:
    headless: bool = True
    default_timeout_ms: int = 30000
    navigation_timeout_ms: int = 30000
    user_agent: Optional[str] = None
    viewport: Optional[Tuple[int, int]] = None

    def __post_init__(self) -> None:
        if self.default_timeout_ms <= 0:
            raise ValueError("default_timeout_ms must be positive.")
        if self.navigation_timeout_ms <= 0:
            raise ValueError("navigation_timeout_ms must be positive.")
        if self.viewport is not None:
            width, height = self.viewport
            if width <= 0 or height <= 0:
                raise ValueError("viewport dimensions must be positive.")

    @classmethod
    def from_env(cls) -> "AgentConfig":
        headless = os.getenv("AI_AGENT_HEADLESS", "true").lower() in {"1", "true", "yes"}
        default_timeout_ms = _parse_int_env("AI_AGENT_DEFAULT_TIMEOUT_MS", 30000)
        navigation_timeout_ms = _parse_int_env("AI_AGENT_NAVIGATION_TIMEOUT_MS", 30000)
        user_agent = os.getenv("AI_AGENT_USER_AGENT")
        viewport = parse_viewport(os.getenv("AI_AGENT_VIEWPORT"))
        return cls(
            headless=headless,
            default_timeout_ms=default_timeout_ms,
            navigation_timeout_ms=navigation_timeout_ms,
            user_agent=user_agent,
            viewport=viewport,
        )


def _parse_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer.") from exc


def parse_viewport(value: Optional[str]) -> Optional[Tuple[int, int]]:
    if not value:
        return None
    try:
        width_str, height_str = value.lower().split("x", maxsplit=1)
        return int(width_str), int(height_str)
    except ValueError as exc:
        raise ValueError("AI_AGENT_VIEWPORT must be in WIDTHxHEIGHT format.") from exc
