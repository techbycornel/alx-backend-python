# fixtures.py

org_payload = {
    "login": "test_org",
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": None}},
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = ["repo1"]
