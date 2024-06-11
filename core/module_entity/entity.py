# Must not import anything from this module. This is a root class.
import math
import pygame.image
import pygame.transform
import core.graphics as graphics
import core.util

# Returns true if the provided circle intersects with the provided line.
# Exact contact (distance exactly equals radius) is considered an intersection.
def intersect_circle_line(circlex, circley, radius, linex1, liney1, linex2, liney2):
  # Intersects directly with endpoint 1
  if core.util.dist(circlex, circley, linex1, liney1) <= radius: return True
  # Intersects directly with endpoint 2
  if core.util.dist(circlex, circley, linex2, liney2) <= radius: return True
  # Projection collision
  colx, coly = core.util.project(circlex, circley, linex1, liney1, linex2, liney2)
  return core.util.dist(colx, coly, circlex, circley) <= radius

# Returns true if the provided circle intersects with the provided axis aligned bounding box.
# Exact contact (distance exactly equals radius) is considered an intersection.
def intersect_circle_aabb(circlex, circley, radius, x1, y1, w, h):
  # Direct corner intersection
  # Top left
  if core.util.dist(circlex, circley, x1, y1) <= radius: return True
  # Top right
  x2 = x1 + w
  y2 = y1
  if core.util.dist(circlex, circley, x2, y2) <= radius: return True
  # Bottom left
  x3 = x1
  y3 = y1 + h
  if core.util.dist(circlex, circley, x3, y3) <= radius: return True
  # Bottom right
  x4 = x2
  y4 = y3
  if core.util.dist(circlex, circley, x4, y4) <= radius: return True
  # AABB intersection
  ax1 = x1 - radius
  ay1 = y1
  ax2 = x4 + radius
  ay2 = y4
  # Circle intersects with the center or a vertical edge (left or right)
  if (circlex >= ax1) and (circlex <= ax2) and (circley >= ay1) and (circley <= ay2): return True
  bx1 = x1
  by1 = y1 - radius
  bx2 = x4
  by2 = y4 + radius
  # Circle intersects with a horizontal edge (top or bottom)
  return (circlex >= bx1) and (circlex <= bx2) and (circley >= by1) and (circley <= by2)

def dot(x1, y1, x2, y2):
  return x1*x2+y1*y2

# Checks if a point is within the bounds of the provided parallelogram.
# The parallelogram must have one point on the origin,
# and be defined by two vectors corresponding to A->B and A->D
def point_in_originated_parallelogram(px, py, ax, ay, bx, by):
  # Orthogonal vectors a' and b'
  apx = -ay
  apy = ax
  bpx = -by
  bpy = bx
  # Oriented vectors a'' and b'' ((a) (d)ouble (p)rime)
  adpsign = core.util.sign(dot(apx, apy, bx, by))
  adpx = adpsign * apx
  adpy = adpsign * apy
  bdpsign = core.util.sign(dot(ax, ay, bpx, bpy))
  bdpx = bdpsign * bpx
  bdpy = bdpsign * bpy
  # Boundary check
  check = dot(adpx, adpy, px, py)
  bound = dot(adpx, adpy, bx, by)
  if not (0 <= check and check <= bound): return False
  check = dot(bdpx, bdpy, px, py)
  bound = dot(ax, bx, bdpx, bdpy)
  return 0 <= check and check <= bound

# Checks if a point is within the bounds of a provided parallelogram.
# px, py: coordinates of the point to check
# ax, ay, etc: coordinates of the four points of the parallelogram, in clockwise order
def point_in_parallelogram(px, py, ax, ay, bx, by, cx, cy, dx, dy):
  return point_in_originated_parallelogram(px - ax, py - ay, bx - ax, by - ay, dx - ax, dy - ay)

# Checks if two lines intersect at any point.
def intersect_line_line_old(x1, y1, x2, y2, x3, y3, x4, y4):
  # Negated Minkowski addition (computational Minkowsky difference)
  # Define parallelogram ABCD
  Ax = x1 - x3
  Ay = y1 - y3
  Bx = x1 - x4
  By = y1 - y4
  Cx = x2 - x4
  Cy = y2 - y4
  Dx = x2 - x3
  Dy = y2 - y3
  # If result contains the origin, there is an intersection.
  return point_in_parallelogram(0, 0, Ax, Ay, Bx, By, Cx, Cy, Dx, Dy)

def intersect_line(x1, y1, x2, y2, x3, y3, x4, y4):
  t_up = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
  t_dn = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
  if t_up < 0 or t_up > t_dn:
    # No intersection
    return None
  u_up = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)
  u_dn = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
  if u_up < 0 or u_up > u_dn:
    # No intersection
    return None
  t = t_up/t_dn
  u = u_up/u_dn
  x = t * (x2 - x1) + x1
  y = t * (y2 - y1) + y1

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
    if this.collisionType == "circle":
      if other.collisionType == "circle":
        return core.util.dist(this.x, this.y, other.x, other.y) <= this.radius + other.radius
      if other.collisionType == "aabb":
        return intersect_circle_aabb(this.x, this.y, this.radius, other.x, other.y, other.w, other.h)
      if other.collisionType == "line":
        return intersect_circle_line(this.x, this.y, this.radius, other.x, other.y, other.x2, other.y2)
    if this.collisionType == "aabb":
      if other.collisionType == "aabb":
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
      if other.collisionType == "circle":
        return intersect_circle_aabb(other.x, other.y, other.radius, this.x, this.y, this.w, this.h)
      if other.collisionType == "line":
        pass
    if this.collisionType == "line":
      if other.collisionType == "circle":
        return intersect_circle_line(other.x, other.y, other.radius, this.x, this.y, this.x2, this.y2)
    # Unsupported case (such as custom collision type)
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

  # Moves an entity by the offset vector
  # Positive y moves the entity forward
  # Positive x moves the entity right
  def move(this, offset = (0, 0)):
    cos = math.cos(this.angle / 180 * math.pi)
    sin = math.sin(this.angle / 180 * math.pi)
    # Forward movement
    this.x += cos * offset[1]
    this.y += sin * offset[1]
    # Lateral movement
    this.x -= sin * offset[0]
    this.y += cos * offset[0]
