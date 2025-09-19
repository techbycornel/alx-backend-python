#!/usr/bin/env python3
"""Module for GithubOrgClient"""

from typing import Any, Dict
from utils import get_json


class GithubOrgClient:
    """GithubOrgClient to interact with GitHub API for an organization"""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self) -> Dict[str, Any]:
        """Return the organization data as a dictionary"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
