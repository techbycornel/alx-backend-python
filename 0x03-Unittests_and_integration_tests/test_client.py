#!/usr/bin/env python3
"""Unit and integration tests for client module"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test .org property"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        expected_url = "https://api.github.com/orgs/test_org/repos"
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": expected_url},
        ):
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test_org/repos",
        ) as mock_url:
            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected,
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            fixtures.org_payload,
            fixtures.repos_payload,
            fixtures.expected_repos,
            fixtures.apache2_repos,
        )
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get"""
        def fake_get(url, *args, **kwargs):
            mock_resp = Mock()
            if url.endswith("/orgs/google"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/repos") or "/repos" in url:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.get_patcher = patch("utils.requests.get", side_effect=fake_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
