import pygame
import core.graphics.main as graphics
from core.globals import lightmode

# Oh gods here we go
# Particles need to cache excessively
# Individual particle data should exist entirely in the form of parallel property arrays, not objects

# Companion class intended to manage the indexing of any circular array data structure in abstract.
class circular_buffer_indexer:
  def __init__(this, capacity):
    this.capacity = capacity
    this.count = 0
    this.writepos = 0
    this.readpos = 0
  
  def pop(this):
    if this.count < 1:
      return -1
    read = this.readpos
    this.readpos = (read + 1) % this.capacity
    this.count -= 1
    return read
  
  def peek(this):
    if this.count < 1:
      return -1
    return this.readpos
  
  def push(this):
    cap = this.capacity
    if this.count >= cap:
      return -1
    write = (this.writepos + 1) % cap
    this.writepos = write
    this.count += 1
    return write

# Base particle system class
class system:
  def __init__(this, renderable, capacity):
    this.indexer = circular_buffer_indexer(capacity) # handler for freed indices
    this.indexer.arr = [0] * capacity
    this.renderable = renderable # object to instance on each particle. Either an image or a function.
    this.itmx = [0] * capacity # particle position x component
    this.itmy = [0] * capacity # particle position y component
    this.itmvx = [0] * capacity # particle velocity x component
    this.itmvy = [0] * capacity # particle velocity y component
    this.itmlifetime = [0] * capacity # particle time to deletion
    this.itmopacity = [1] * capacity # particle opacity; if 0, particle is autoculled
    this.itmdopacity = [0] * capacity # change in particle opacity per second
    this.itmvalid = [False] * capacity # particle activity status

  def update(this, dt):
    if lightmode: return
    # Caching variables to avoid unnecessary dictionary accesses
    indexer = this.indexer
    itmx = this.itmx
    itmy = this.itmy
    itmvx = this.itmvx
    itmvy = this.itmvy
    life = this.itmlifetime
    opacity = this.itmopacity
    fade = this.itmdopacity
    valid = this.itmvalid
    # Update all particles
    for i in range(0, indexer.capacity):
      if valid[i]:
        # Physics updates
        itmx[i] += itmvx[i] * dt
        itmy[i] += itmvy[i] * dt
        # Property updates
        life[i] -= dt
        opacity[i] += fade[i] * dt
        # Cull dead particles
        if life[i] <= 0 or opacity[i] <= 0:
          # Invalidate particle slot
          valid[i] = False
          # Push slot to pool
          indexer.arr[indexer.writepos] = i
          indexer.push(i)

  def draw(this, surface = None):
    if lightmode: return
    # Validate target surface
    if surface == None:
      surface = graphics.check()
    if surface == None:
      return
    # Cache variables to avoid unnecessary dictionary accesses
    renderable = this.renderable
    valid = this.itmvalid
    # Branch: render type
    if callable(renderable):
      # Manual render type (user supplied)
      # renderable is a function
      for i in range(0, this.indexer.capacity):
        if valid[i]:
          renderable(this, i, surface)
    else:
      # Handled render type (sprite supplied)
      # renderable is an image
      itmx = this.itmx
      itmy = this.itmy
      opacity = this.itmopacity
      for i in range(0, this.indexer.capacity):
        if valid[i]:
          renderable.setOpacity(opacity(i))
          surface.blit(renderable, (itmx[i], itmy[i]))

# Extended particle system using more advanced image caching
class systemcached(system):
  def __init__(this, capacity):
    system.__init__(this, capacity)
    this.itmtheta = [0] * capacity # particle rotation in degrees
    this.itmvtheta = [0] * capacity # particle rotational velocity in d/s
    this.itmscale = [1] * capacity # particle scale factor; if 0, particle is autoculled
    this.itemdscale = [0] * capacity # change in scale factor each second
