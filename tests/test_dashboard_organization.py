# tests/test_dashboard_organization.py

import pytest
from src.reportify.model.dashboard.dashboard_organization import OrganizationalDashboard
import os
import pandas as pd
class FakeCacheItem:
    def to_pandas(self):
        return pd.DataFrame({
            "id": [1, 2],
            "title": ["Issue 1", "Issue 2"]
        })
def test_OrganizationalDashboard_env_variables(monkeypatch):
    # Simula variáveis de ambiente
    monkeypatch.setenv("GITHUB_TOKEN", "fake_token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "fake/repo")


    fake_cache = {
        "issues": FakeCacheItem(),
    }
    dev = OrganizationalDashboard(save_func=lambda x, y: None, token=os.getenv("GITHUB_TOKEN"), repo=os.getenv("GITHUB_REPOSITORY"),cache=fake_cache)
    
    assert dev.token == "fake_token"
    assert dev.repo == "fake/repo"
    