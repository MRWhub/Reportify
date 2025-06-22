# tests/test_dashboard_developer.py

import pytest
from src.reportify.model.dashboard.dashboard_developer import DeveloperStats
import os


def test_developerstats_env_variables(monkeypatch):
    # Simula variáveis de ambiente
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "fake/repo")

    dev = DeveloperStats(save_func=lambda x, y: None, token=os.getenv("GITHUB_TOKEN"), repo=os.getenv("GITHUB_REPOSITORY"))
    
    assert dev.token == "fake_token"
    assert dev.repository == "fake/repo"
