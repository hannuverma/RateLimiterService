from dataclasses import dataclass
 
from redis.asyncio import Redis
 
from ..limiters.base import Decision, RateLimiter
from ..limiters.registry import build_limiter
from .keys import build_key
from .models import Rule
from .rules import RuleProvider

class RuleNotFound(Exception):
    pass

class InvalidCost(Exception):
    pass

@dataclass
class CheckResult:
    rule: Rule
    decision: Decision

class RateLimitService:

    def __init__(self, r: Redis, rules: RuleProvider):
        self._r = r
        self._rules = rules
        self._limiters: dict[tuple, RateLimiter] = {}

    def _limiter_for(self, rule: Rule) -> RateLimiter:
        # keyed by the full rule definition so an edited rule gets a fresh limiter (M3)
        k = (rule.name, rule.algorithm, rule.limit, rule.window_ms)
        if k not in self._limiters:
            self._limiters[k] = build_limiter(rule.algorithm, self._r, rule.limit, rule.window_ms)
        return self._limiters[k]
 
    async def check(self, rule_name: str, identifier: str, cost: int = 1, tenant: str = "default") -> CheckResult:
        rule = self._rules.get(rule_name)
        if rule is None:
            raise RuleNotFound(rule_name)
        if cost > rule.limit:
            raise InvalidCost(f"cost {cost} exceeds the rule's limit {rule.limit}")
        key = build_key(tenant, rule.name, identifier)
        decision = await self._limiter_for(rule).allow(key, cost)
        return CheckResult(rule, decision)