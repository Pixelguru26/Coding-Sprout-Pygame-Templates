import math, pygame
from core.module_entity.entity import entity
from core.globals import bullets, images

class bullet(entity):
  # Entity type used to distinguish subclasses
  type = "bullet_base"

  def __init__(this, team, x, y, angle, damage, speed, radius = 1):
    entity.__init__(this, team, x, y, angle)
    this.sprite = images["bullet_base"]
    this.damage = damage
    this.speed = speed
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

# Fires a bullet from this entity.
# Valid teams are: "player", "enemy", "none", "all"; indicating who will be excluded from collisions.
# Optional offset creates the bullet just ahead of the entity, potentially preventing self-annihilation.
def __shoot(this, variant = "base", offset = False):
  ret = None

  # Create abstract bullet entity
  if variant == "base":
    ret = bullet(this.team, this.x, this.y, this.angle, 100, 1024)
  
  # Offset if applicable
  if offset and this.collisionType == "circle" and ret != None and ret.collisionType == "circle":
    ret.forward(this.radius + ret.radius + 1) # +1 for extra padding safety as most intersections are inclusive.
  
  # Add bullet to world
  if ret != None:
    bullets.append(ret)
entity.shoot = __shoot