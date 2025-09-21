#!/usr/bin/env python3
"""
Client module
"""
import requests
from utils import get_json


class GithubOrgClient:
    """GithubOrgClient class to interact with GitHub API"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name):
        self._org_name = org_name

    @property
    def org(self):
        """Fetch organization data"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self):
        """Return the public repos URL"""
        return self.org.get("repos_url")

    def public_repos(self, license_key=None):
        """List public repos, optionally filtered by license"""
        repos = get_json(self._public_repos_url)
        repo_names = [repo["name"] for repo in repos]
        if license_key is None:
            return repo_names
        return [
            repo["name"]
            for repo in repos
            if self.has_license(repo, license_key)
        ]

    @staticmethod
    def has_license(repo, license_key):
        """Check if repo has given license"""
        try:
            return repo["license"]["key"] == license_key
        except (KeyError, TypeError):
            return False
