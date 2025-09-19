#!/usr/bin/env python3
"""
Client module for GithubOrgClient
"""

from utils import get_json


class GithubOrgClient:
    """Github Org client class"""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self) -> dict:
        """Return the org info as JSON"""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")
