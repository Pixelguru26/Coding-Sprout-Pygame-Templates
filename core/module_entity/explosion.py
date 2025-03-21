import math, pygame
import core.graphics as graphics
from core.module_entity.bullet import bullet
from core.module_entity.entity import entity
from core.globals import images, bulletque

class explosion(bullet):
  type = "explosion_base"
  default_damage = 60

  def __init__(this, team, x, y, radius = -1):
    if radius < 0:
      radius = images["splode"].get_width()/2
    bullet.__init__(this, team, x, y, 0, radius)
    this.sprite = images["splode"]
    this.attack = explosion.default_damage
    this.speed = 0
    this.hitmem = {}
  
  def update(this, dt):
    bullet.update(this, dt)
    if this.age > images["splode"].duration:
      this.delete()

  def impact(this, target):
    if not (this.age > this.sprite.duration):
      if not (target.unitid in this.hitmem):
        target.damage(this.attack)
        this.hitmem[target.unitid] = True

class lance(bullet):
  type = "bullet_lance"
  default_damage = 60

  def __init__(this, team, x, y, angle):
    bullet.__init__(this, team, x, y, angle)
    this.scale = 0.5
    length = images["lance"].get_width()/2
    this.sprite = images["lance"]
    this.collisionType = "line"
    this.x = x
    this.y = y
    this.x2 = x + this.cos * length
    this.y2 = y + this.sin * length
    this.attack = lance.default_damage
    this.speed = 0
    this.hitmem = {}
  
  # def draw(this):
  #   bullet.draw(this)
  #   pygame.draw.line(graphics.check(), (255, 255, 255, 255), (this.x, this.y), (this.x2, this.y2), 4)
  
  def update(this, dt):
    bullet.update(this, dt)
    if this.age > this.sprite.duration:
      this.delete()
    
  def impact(this, target):
    if not (this.age > this.sprite.duration):
      if not (target.unitid in this.hitmem):
        target.damage(this.attack)
        this.hitmem[target.unitid] = True

bullet.variants["explosion"] = explosion
bullet.variants["lance"] = lance

def explode(this: bullet):
  this.damage(1000)
  bulletque.append(explosion(this.team, this.x, this.y))
entity.explode = explode