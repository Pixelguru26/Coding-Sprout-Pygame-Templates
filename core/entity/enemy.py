from core.entity.entity import entity as entity

class enemy(entity):
  def __init__(this, variant, x, y, angle, radius = 32):
    entity.__init__(this, "enemy", variant, x, y, angle, 128/512)
    this.health = 100
    this.radius = radius
