
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local cost = tonumber(ARGV[3])

local t = redis.call('TIME')
local now = t[1] * 1000 + math.floor(t[2] / 1000)

local curr_id = math.floor(now / window)
local elapsed = now % window

local curr_key = KEYS[1] .. ':' .. curr_id
local prev_key = KEYS[1] .. ':' .. (curr_id - 1)

local estimated = (prev * (window - elapsed) / window) + curr

if estimated + cost <= limit then
    redis.call("INCRBY", curr_key, cost)
    redis.call("PEXPIRE", curr_key, window*2)

    return {1, math.floor(limit - estimated - cost), 0}
end

if cost > limit then
    return {0, 0, window}
end

local remaining = math.max(0, limit - estimated)

-- When does it free up? 1) inside this window, as prev's weight decays
local needed  = estimated + cost - limit
local to_end  = window - elapsed
if prev > 0 then
  local dt = needed * window / prev
  if dt <= to_end then
    return {0, remaining, math.ceil(dt)}
  end
end
-- 2) otherwise in the next window, where curr becomes prev (assuming no new traffic)
local allowed_curr = limit - cost
local e = 0
if curr > allowed_curr then
  e = 1 - allowed_curr / curr
end
return {0, remaining, to_end + math.ceil(e * window)}