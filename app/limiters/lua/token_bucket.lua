
local key      = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate     = tonumber(ARGV[2])
local cost     = tonumber(ARGV[3])

local t   = redis.call('TIME')
local now = t[1] * 1000 + math.floor(t[2] / 1000)

local d      = redis.call('HMGET', key, 'tokens', 'ts')
local tokens = tonumber(d[1]) or capacity       -- new key = full bucket
local ts     = tonumber(d[2]) or now

tokens = math.min(capacity, tokens + math.max(0, now - ts) * rate / 1000)

local allowed = 0
local retry   = 0
if tokens >= cost then
  tokens  = tokens - cost
  allowed = 1
elseif cost > capacity then
  retry = -1                                    -- impossible request
else
  retry = math.ceil((cost - tokens) / rate * 1000)
end

redis.call('HSET', key, 'tokens', tokens, 'ts', now)   -- save ts even when blocked
redis.call('PEXPIRE', key, math.ceil(capacity / rate * 1000) * 2)
return {allowed, math.floor(tokens), retry}