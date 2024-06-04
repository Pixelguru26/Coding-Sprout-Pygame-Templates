# Must not import anything from this module. This is a root class.
import math
import pygame.image
import pygame.transform
import core.graphics as graphics

class entity:
  collisionTypes = {
    "circle": "circle",
    "aabb": "aabb",
    "line": "line"
  }
  # Entity type used to distinguish subclasses
  type = "entity"

  def __init__(this, team = "none", x = 0, y = 0, angle = 0, scale = 1, collisionType = "circle", a = 0, b = 0):
    this.team = team
    this.x = x
    this.y = y
    this.angle = angle
    this.last_angle = angle
    this.scale = scale
    this.last_scale = scale
    this.speed = 100
    # Each collision type has its own dimension argument overload.
    this.collisionType = collisionType
    if collisionType == "circle":
      this.radius = a
    elif collisionType == "aabb":
      this.w = a
      this.h = b
    elif collisionType == "line":
      this.x2 = a
      this.y2 = b
    this.alive = True
    # Source surface for sprites
    this.sprite = None
    # Cache for storing current rotated and scaled sprite
    this.sprite_cache = None
    this.update_graphics(True)
  
  # This performs no ai functions, but is necessary for proper optimization and visual behavior.
  def update(this, dt):
    this.update_graphics()
    pass

  
  # Update cached sprite when rotated or scaled.
  # Only updates when necessary.
  # Provide "True" as a second argument to force an update with no checks.
  def update_graphics(this, override = False):
    doUpdate = False
    # Always necessary
    if this.sprite == None:
      doUpdate = True
      this.sprite = pygame.image.load(f"assets\image\error.png")
    if override or this.sprite != this.last_sprite:
      doUpdate = True
      this.last_sprite = this.sprite
    # Automatically update cache for rotations
    if override or this.angle != this.last_angle:
      doUpdate = True
      # Updating cached trig values (future optimization)
      angle = this.angle/180 * math.pi
      this.cos = math.cos(angle)
      this.sin = math.sin(angle)
      this.last_angle = this.angle
    # Automatically update cache for scaling
    if override or this.scale != this.last_scale:
      doUpdate = True
      this.last_scale = this.scale

    # If any property has changed, update sprite cache appropriately.
    # Also fires if the sprite cache is still uninitialized.
    if doUpdate or this.sprite_cache == None:
      # Update cached graphics
      this.sprite_cache = pygame.transform.rotozoom(this.sprite, -this.angle, this.scale)
  
  # Renders cached graphics by default. Does not update cache.
  def draw(this):
    if this.collisionType == "circle":
      graphics.blit_centered(this.sprite_cache, this.x, this.y)
    else:
      graphics.blit(this.sprite_cache, this.x, this.y)

  # Checks if this entity intersects another using proper collision types.
  # Includes exact contact (distance = 0)
  # Returns False if collision types are unimplemented.
  def intersects(this, other):
    if this.collisionType == entity.collisionTypes["circle"]:
      if other.collisionType == entity.collisionTypes["circle"]:
        # Simple circle-circle intersection
        dx = other.x - this.x
        dy = other.y - this.y
        dist = math.sqrt(dx*dx+dy*dy)
        return dist <= this.radius + other.radius
      if other.collisionType == entity.collisionTypes["aabb"]:
        # Approximate circle-aabb intersections as pure aabb intersections.
        # Good enough for culling, which is all we need right now.
        return this.x >= other.x + this.radius and this.y >= other.y + this.radius and this.x <= other.x + other.w - this.radius and this.y <= other.y + other.h - this.radius
    if this.collisionType == entity.collisionTypes["aabb"]:
      if other.collisionType == entity.collisionTypes["aabb"]:
        # AABB intersection
        l1 = this.x
        r1 = this.x + this.w
        u1 = this.y
        d1 = this.y + this.h
        l2 = other.x
        r2 = other.x + other.w
        u2 = other.y
        d2 = other.y + other.y
        return l1 <= r2 and r1 >= l2 and u1 <= d2 and d1 >= u2
      if other.collisionType == entity.collisionTypes["circle"]:
        # Approximate circle-aabb intersections as pure aabb intersections.
        # Good enough for culling, which is all we need right now.
        return other.x >= this.x + other.radius and other.y >= this.y + other.radius and other.x <= this.x + this.w - other.radius and other.y <= this.y + this.h - other.radius
    # Lines not yet supported
    return False
  
  def delete(this):
    # This will be used for death animations.
    # Name chosen to alarm fewer parents.
    this.alive = False
  
  # Turtle capabilities
  # Moves the entity forward by the specified number of pixels.
  def forward(this, amount = 1):
    this.x += math.cos(this.angle / 180 * math.pi) * amount
    this.y += math.sin(this.angle / 180 * math.pi) * amount
  
  # Moves the entity backward by the specified number of pixels.
  # Equivalent to this.forward(-amount)
  def backward(this, amount = 1):
    this.forward(-amount)
  
  # Moves the entity along the vector 90 degrees clockwise of its angle.
  def right(this, amount = 1):
    this.x += math.cos((this.angle + 90) / 180 * math.pi) * amount
    this.y += math.sin((this.angle + 90) / 180 * math.pi) * amount

  # Moves the entity along the vector 90 degrees counter-clockwise of its angle.
  # Equivalent to this.right(-amount)
  def left(this, amount = 1):
    this.right(-amount)

  # Rotates clockwise by the specified number of degrees. (90 by default)
  def rotate(this, amount = 90):
    this.angle += amount
    angle = this.angle / 180 * math.pi
    this.cos = math.cos(angle)
    this.sin = math.sin(angle)

  # Rotates clockwise by the specified number of degrees. (90 by default)
  def turnRight(this, amount = 90):
    this.rotate(amount)
  
  # Rotates counter-clockwise by the specified number of degrees. (90 by default)
  # Equivalent to this.turnRight(-amount)
  def turnLeft(this, amount = 90):
    this.rotate(-amount)