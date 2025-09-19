#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")  # patch get_json in the client module
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value"""
        # Set what the mocked get_json should return
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called once with the right URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        # Assert that the result is what we mocked
        self.assertEqual(result, expected_payload)
