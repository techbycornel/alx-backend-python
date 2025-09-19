#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient

class TestGithubOrgClient(TestCase):
    """Unit tests for GithubOrgClient"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected list of repo names"""

        # Example payload returned by get_json
        mock_get_json.return_value = [
            {"name": "repo1"}, 
            {"name": "repo2"}
        ]

        client = GithubOrgClient("test_org")

        # Patch the _public_repos_url property with a context manager
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            repos = client.public_repos()

            # Check that the repos list matches the mocked payload
            self.assertEqual(repos, ["repo1", "repo2"])

            # Check that the mocks were called exactly once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")

class TestGithubOrgClient(TestCase):

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean"""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

class TestIntegrationGithubOrgClient(TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get to return fixture payloads"""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        # Side effect to return different payloads depending on URL
        def side_effect(url, *args, **kwargs):
            mock_resp = unittest.mock.Mock()
            if url.endswith("/orgs/google"):
                mock_resp.json.return_value = cls.org_payload
            else:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, mock_get_json, org_name):
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that public_repos_url property returns the correct URL"""
        client = GithubOrgClient("test_org")
        expected_url = "https://api.github.com/orgs/test_org/repos"
        self.assertEqual(client._public_repos_url, expected_url)