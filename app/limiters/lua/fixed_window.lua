

local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local cost = tonumber(ARGV[3])

local t = redis.call("TIME")
local now = t[1] * 1000 + math.floor(t[2] / 1000)


local window_id = math.floor(now / window)
local key = KEYS[1] .. ":" .. window_id

local count = tonumber(redis.call('GET', key) or 0)

if count + cost <= limit then
    count = redis.call('INCRBY', key, cost)
    redis.call('PEXPIRE', key, window)
    return {1, limit - count, 0}
end

local retry = ((window_id + 1) * window) - now

return {0, math.max(0, limit - count), retry}
