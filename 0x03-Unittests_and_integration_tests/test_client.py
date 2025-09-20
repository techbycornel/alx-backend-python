#!/usr/bin/env python3
"""
Unit and Integration tests for client module
"""

import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from client import get_json  # needed for optional license filtering


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            client = GithubOrgClient("test_org")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @patch("client.get_json")
    def test_public_repos_url(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test_org/repos"
            client = GithubOrgClient("test_org")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test_org/repos"
            )

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Patch _public_repos_url to return a valid URL
        cls.url_patcher = patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        )
        cls.mock_url = cls.url_patcher.start()

        def get_side_effect(url, *args, **kwargs):
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data
                def json(self):
                    return self._json_data

            if url.endswith("/repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(cls.org_payload)

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
        cls.url_patcher.stop()



@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Patch _public_repos_url to return a valid URL
        cls.url_patcher = patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        )
        cls.mock_url = cls.url_patcher.start()

        def get_side_effect(url, *args, **kwargs):
            class MockResponse:
                def __init__(self, json_data):
                    self._json_data = json_data
                def json(self):
                    return self._json_data

            if url.endswith("/repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(cls.org_payload)

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()
        cls.url_patcher.stop()


if __name__ == "__main__":
    unittest.main()
