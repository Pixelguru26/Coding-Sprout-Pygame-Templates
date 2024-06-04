import random
from core.globals import entities, screen

# An instance of timer is called a "spawn"
# spawns contains all currently active instances and registers them to receive update ticks.
spawns = []

# An advanced repeating trigger class.
# Executes the provided function at regular (or irregular) intervals with sub-frame compensation.
# The function should receive a single argument, subdt, which represents the time since the beginning of the trigger frame, in seconds.
class timer:
  def __init__(this, minDelay, maxDelay, fn):
    this.minDelay = minDelay
    this.maxDelay = maxDelay
    this.fn = fn
    
    this.time = 0
    this.delay = random.random() * (maxDelay - minDelay) + minDelay
  
  def update(this, dt):
    start = this.time
    this.time += dt

    while this.time >= this.delay:
      this.time -= this.delay
      # dt sub is the time since the start of the trigger frame in seconds.
      # This can be used to compensate for cases where multiple events happen in a single frame.
      subdt = this.delay - start
      this.fn(subdt)

  # Registers this timer to the spawns list if it is not already present.
  def register(this):
    if this in spawns: return
    spawns.append(this)
  
  # Removes this timer from the spawns list and resets it.
  def remove(this):
    this.time = 0
    spawns.remove(this)

# A minor extension to the timer specialized for common spawn cases
class spawnTimer(timer):
  def __init__(this, entityType, minDelay, maxDelay, spawnFn = None):
    if spawnFn == None:
      spawnFn = this.spawnFn
    timer.__init__(this, minDelay, maxDelay, spawnFn)
    this.entityType = entityType
  
  # Default spawn function that works well enough for most enemies
  def spawnFn(this, subdt):
    ret = this.entityType(0, 0, 90)
    x = 0
    y = 0
    if ret.collisionType == "circle":
      x = random.uniform(ret.radius, screen.w - ret.radius * 2)
      y = -ret.radius
    elif ret.collisionType == "aabb":
      y = -ret.h
      x = random.uniform(0, screen.w - ret.w)
    # Line collisions don't have a sensible default other than (0, 0)
    ret.x = x
    ret.y = y
    entities.append(ret)
    # Perform a PARTIAL update tick as the entities are created, allowing them to appear correctly on long frames
    # Prevents entities from clustering together in a wave any time the game lags
    ret.update(subdt)

# Propagate update to individual spawn types
# Allows the controller to include multiple spawns at different intervals
def update(dt):
  for spawn in spawns:
    spawn.update(dt)

# Utility function which constructs and registers a varied spawn
def addBasic(entityType, minDelay, maxDelay):
  ret = spawnTimer(entityType, minDelay, maxDelay)
  spawns.append(ret)
  return ret
