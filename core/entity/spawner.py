import random
from globals import entities
from globals import screen

spawns = []

# An advanced repeating trigger class.
# Executes the provided function at regular (or irregular) intervals with sub-frame compensation.
# The function should receive a single argument, dtsub, which represents the time since the beginning of the trigger frame, in seconds.
class timer:
  def __init__(this, minDelay, maxDelay, fn):
    this.minDelay = minDelay
    this.maxDelay = maxDelay
    this.fn = fn

    this.time = 0
    this.delay = random.range(minDelay, maxDelay)
  
  def update(this, dt):
    start = this.time
    this.time += dt

    while this.time >= this.delay:
      this.time -= this.delay
      # dt sub is the time since the start of the trigger frame in seconds.
      # This can be used to compensate for cases where multiple events happen in a single frame.
      dtsub = this.delay - start
      this.fn(dtsub)

# A minor extension to the timer specialized for common spawn cases
class spawnClock(timer):
  def __init__(this, entityType, minDelay, maxDelay, spawnFn = None):
    if spawnFn == None:
      spawnFn = this.spawnFn
    timer.__init__(this, minDelay, maxDelay, spawnFn)
    this.entityType = entityType
  
  def spawnFn(this, subdt):
    ret = this.entityType()
    x = 0
    y = 0
    if ret.collisionType == "circle":
      x = random.range(ret.radius, screen.w + ret.radius)
      y = -ret.radius
    elif ret.collisionType == "aabb":
      y = -ret.h
    entities.append(ret)
    ret.update(subdt)

def addBasic(entityType):
  pass


