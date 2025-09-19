# utils.py

from typing import Mapping, Any, Sequence
import requests

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map with a sequence of keys."""
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> dict:
    """Fetch JSON from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Decorator to cache a method’s result."""
    attr_name = "_memoized_" + fn.__name__

    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
