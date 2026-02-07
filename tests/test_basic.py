import pytest
from src.agent.core import Agent

def test_agent_initialization():
    agent = Agent(headless=True)
    assert agent is not None
    assert agent.browser_manager is not None

def test_agent_run():
    agent = Agent(headless=True)
    # We use a very reliable site for testing to avoid flakiness, or mock it.
    # For now, let's just test against example.com as a live integration test.
    title = agent.run("https://example.com")
    assert "Example Domain" in title
