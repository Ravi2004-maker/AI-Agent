import pytest

from src.agent import core
from src.agent.config import AgentConfig

def test_agent_initialization():
    agent = core.Agent(config=AgentConfig(headless=True))
    assert agent is not None
    assert agent.browser_manager is not None

class FakePage:
    def title(self):
        return "Example Domain"


class FakeBrowserManager:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.page = FakePage()
        self.started = False
        self.got_url = None
        self.timeout_ms = None
        self.closed = False

    def start(self):
        self.started = True

    def goto(self, url: str, timeout_ms: int = None):
        self.got_url = url
        self.timeout_ms = timeout_ms

    def close(self):
        self.closed = True


def test_agent_run(monkeypatch):
    monkeypatch.setattr(core, "BrowserManager", FakeBrowserManager)
    agent = core.Agent(config=AgentConfig(headless=True))
    title = agent.run("https://example.com", timeout_ms=123)
    assert title == "Example Domain"
    assert agent.browser_manager.got_url == "https://example.com"
    assert agent.browser_manager.timeout_ms == 123


def test_agent_run_invalid_url():
    agent = core.Agent(config=AgentConfig(headless=True))
    with pytest.raises(ValueError):
        agent.run("not-a-valid-url")
