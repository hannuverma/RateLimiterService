from typing import Protocol
 
from .models import Rule
 

class RuleProvider(Protocol):
    def get_rule(self, name:str) -> Rule: ...

class StaticRules:
    """Hardcoded rules for M2. M3 replaces this with a Postgres-backed provider (same interface)."""
 
    def __init__(self, rules: list[Rule]):
        self._rules = {r.name: r for r in rules}
 
    def get(self, name: str) -> Rule | None:
        return self._rules.get(name)
 
 
DEFAULT_RULES = [
    Rule(name="api_default", algorithm="token_bucket", limit=100, window_ms=60_000),
    Rule(name="search", algorithm="sliding_counter", limit=20, window_ms=60_000),
    Rule(name="login", algorithm="sliding_log", limit=5, window_ms=300_000),
    Rule(name="per_ip", algorithm="fixed_window", limit=60, window_ms=60_000),
]
