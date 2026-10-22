
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local cost = tonumber(ARGV[3])

local key = KEYS[1]

local t = redis.call('TIME')
local now = t[1] * 1000 + math.floor(t[2] / 1000)

local now_us = t[1] * 1000 + t[2]

redis.call("ZREMRANGEBYSCORE", key, "-inf", now_us - window)

local count = redis.call("ZCARD", key)

if cost + count <= limit then
    for i = 1, cost do
        redis.call('ZADD', key, now, now_us .. '-' .. (count + i))
    end

    redis.call("PEXPIRE", key, window)

    local rem = limit - (count + cost)

    return {1, rem, 0}
end

if cost > limit then
    return {0, 0, window}
end


local idx = cost + count - limit
local entry  = redis.call('ZRANGE', key, idx - 1, idx - 1, 'WITHSCORES')
local retry  = math.max(1, tonumber(entry[2]) + window - now)
return {0, math.max(0, limit - count), retry}