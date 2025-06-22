# tests/test_dashboard_repository.py

import pytest
from src.reportify.model.dashboard.dashboard_team_graph import CollaborationGraph
import os


def test_team_stats_graph_env_variables(monkeypatch):
    # Simula variáveis de ambiente
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "fake/repo")

    dev = CollaborationGraph(save_func=lambda x, y: None, token=os.getenv("GITHUB_TOKEN"), repo=os.getenv("GITHUB_REPOSITORY"))
    
    assert dev.token == "fake_token"
    assert dev.repository == "fake/repo"