from module_entity.entity import entity as __entity
import core.graphics as __graphics
from core.graphics.animg import animg as __animg

class effectobj(__entity):
  def __init__(this, img, x, y, angle = 0, scale = 1):
    __entity.__init__(this, "none", x, y, angle, scale)
    this.img = img
    if not isinstance(img, __animg):
      print("Effect object has no image")
      return
    
  def update(this, dt):
    pass

  def draw(this):
    surf = __graphics.check()
    if surf == None: return
    this.img.drawframe_centered(surf, this.x, this.y)

