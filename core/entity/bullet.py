from core.entity.entity import entity as entity
import math
import pygame.image
from core.globals import bullets

class bullet(entity):
  def __init__(this, team, x, y, angle, damage, speed, radius = 1):
    entity.__init__(this, team, "base", x, y, angle)
    this.damage = damage
    this.speed = speed
    this.radius = radius
    this.sprite = pygame.image.load(f"assets\image\projectile\\bullet_base.png")
    this.update_graphics()
  
  def update(this, dt):
    cos = math.cos(this.angle / 180 * math.pi)
    sin = math.sin(this.angle / 180 * math.pi)
    this.x += cos * this.speed * dt
    this.y += sin * this.speed * dt
  
  def impact(this, target):
    target.health -= this.damage
    this.alive = False

# Fires a bullet from this entity.
# Valid teams are: "player", "enemy", "none", "all"; indicating who will be excluded from collisions.
# Optional offset creates the bullet just ahead of the entity, potentially preventing self-annihilation.
def __fire(this, team = "enemy", variant = "base", offset = False):
  bullet = None

  # Create abstract bullet entity
  if variant == "base":
    bullet = bullet(team, this.x, this.y, this.angle, 100, 1024)
  
  # Offset if applicable
  if offset and this.collisionType == "circle" and bullet != None and bullet.collisionType == "circle":
    bullet.forward(this.radius + bullet.radius + 1) # +1 for extra padding safety as most intersections are inclusive.
  
  # Add bullet to world
  if bullet != None:
    bullets.append(bullet)
entity.fire = __fire

