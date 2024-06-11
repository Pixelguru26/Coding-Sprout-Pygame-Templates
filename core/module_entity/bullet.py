import math, pygame
from core.module_entity.entity import entity
from core.globals import bullets, images

class bullet(entity):
  # Entity type used to distinguish subclasses
  type = "bullet_base"
  default_speed = 1024
  default_damage = 100

  def __init__(this, team, x, y, angle, radius = 1):
    entity.__init__(this, team, x, y, angle)
    this.sprite = images["bullet_base"]
    this.damage = bullet.default_damage
    this.speed = bullet.default_speed
    this.radius = radius
    this.update_graphics()
  
  def update(this, dt):
    # cos = math.cos(this.angle / 180 * math.pi)
    # sin = math.sin(this.angle / 180 * math.pi)
    # this.x += cos * this.speed * dt
    # this.y += sin * this.speed * dt
    this.forward(this.speed * dt)
  
  # Deals damage to the target and destroys this bullet.
  def impact(this, target):
    target.health -= this.damage
    this.alive = False

  # Deals damage to the target and destroys this bullet.
  # Checks team alignment first.
  def touch(this, target):
    if target.team != "none":
      if target.team == this.team or target.team == "all":
        return
    this.impact(target)

class rocket(bullet):
  # Rockets are launched backward and downward to give the impression of being dropped
  # Then they accelerate rapidly forward and upward.
  # Acceleration is in units of pixels per second per second
  # Vertical damping is the upward acceleration, which can only decrease fall speed to -100
  initial_fall_speed = 400
  vertical_damping = 1024
  initial_speed = -100
  acceleration = 2048
  default_damage = 200
  type = "bullet_rocket"

  def __init__(this, team, x, y, angle):
    bullet.__init__(this, team, x, y, angle)
    this.speed = rocket.initial_speed
    this.fallspeed = rocket.initial_fall_speed
    this.damage = rocket.default_damage
    this.sprite = images["bullet_rocket"]
    this.update_graphics()

  def update(this, dt):
    this.speed += dt * rocket.acceleration
    this.y += dt * this.fallspeed
    this.fallspeed -= rocket.vertical_damping * dt
    if this.fallspeed < -100: this.fallspeed = 0
    bullet.update(this, dt)

# Fires a bullet from this entity.
# Valid teams are: "player", "enemy", "none", "all"; indicating who will be excluded from collisions.
def __shoot(this, variant = "base", offset = (0, 0)):
  ret = None

  # Create abstract bullet entity
  if variant == "base":
    ret = bullet(this.team, this.x, this.y, this.angle)
  elif variant == "rocket":
    ret = rocket(this.team, this.x, this.y, this.angle)
  
  if ret != None:
    ret.move(offset)

    # Add bullet to world
    bullets.append(ret)
    # Return reference to fired bullet, in case it's needed
    return ret
entity.shoot = __shoot