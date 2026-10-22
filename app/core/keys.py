def build_key(tenant: str, rule: str, identifier: str) -> str:
    """rl:{tenant}:{rule}:{identifier}
 
    Tenant prefix = one customer can never touch another's counters.
    (M4: for Redis Cluster, wrap the part that must stay together in {...} hash tags.)
    """
    return f"rl:{tenant}:{rule}:{identifier}"