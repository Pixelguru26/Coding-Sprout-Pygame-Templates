from core.module_entity.entity import entity
from core.globals import images

class enemy(entity):
  # Entity type used to distinguish subclasses
  type = "enemy_base"

  def __init__(this, x, y, angle = 90, radius = 32, speed = 100):
    entity.__init__(this, "enemy", x, y, angle, 128/512)
    this.sprite = images["enemy_base"]
    this.health = 100
    this.radius = radius
    this.speed = speed
    this.update_graphics()
  
  def update(this, dt):
    entity.update(this, dt)
    this.forward(this.speed * dt)
