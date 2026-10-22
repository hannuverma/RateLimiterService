from .fixed_window import FixedWindow
from .sliding_counter import SlidingCounter
from .sliding_log import SlidingLog
from .token_bucket import TokenBucket

# algorithm name (as stored in a rule) -> class
LIMITERS = {
    "fixed_window": FixedWindow,
    "sliding_log": SlidingLog,
    "sliding_counter": SlidingCounter,
    "token_bucket": TokenBucket,
}