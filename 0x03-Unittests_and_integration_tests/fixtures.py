# fixtures.py

org_payload = {
    "login": "my_org",
    "id": 1,
    "node_id": "MDQ6VXNlcjE=",
    "url": "https://api.github.com/orgs/my_org",
    "repos_url": "https://api.github.com/orgs/my_org/repos",
    "events_url": "https://api.github.com/orgs/my_org/events",
    "hooks_url": "https://api.github.com/orgs/my_org/hooks",
    "issues_url": "https://api.github.com/orgs/my_org/issues",
    "members_url": "https://api.github.com/orgs/my_org/members{/member}",
    "public_members_url": "https://api.github.com/orgs/my_org/public_members{/member}",
    "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
    "description": "Fake organization payload for testing"
}

repos_payload = [
    {"id": 123, "name": "repo1", "license": {"key": "mit"}},
    {"id": 456, "name": "repo2", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2"]

apache2_repos = ["repo1"]
