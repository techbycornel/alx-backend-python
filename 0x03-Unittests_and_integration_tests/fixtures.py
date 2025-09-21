# fixtures.py

org_payload = {
    "login": "test_org",
    "repos_url": "https://api.github.com/orgs/test_org/repos",
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
]

expected_repos = ["repo1", "repo2"]

apache2_repos = ["repo1"]
