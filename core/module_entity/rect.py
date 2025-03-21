from core.module_entity.entity import entity
import core.graphics as graphics
import pygame as pg
from core.globals import entityque

class rect(entity):
  def __init__(this, x=0, y=0, w=0, h=0, fill = (25, 128, 64, 255)):
    super().__init__("none", x, y, 0, 1, "aabb", w, h)
    this.fill = fill
    this.round = 2
    this.line = fill
    this.textcolor = (0, 50, 0, 255)
    this.thickness = 2
    this.__text = ""
    this.__textsurf = None
    this.__font = None
    entityque.append(this)

  def __changetext(this, val):
    if val != this.__text:
      if this.__font == None:
        this.__font = pg.font.Font(None, 24)
      this.__text = val
      this.__textsurf = this.__font.render(str(this.__text), True, this.textcolor)

  text = property(
    fget=lambda this : this.__text,
    fset = __changetext,
    fdel = lambda this : delattr(this, "__text"),
    doc = "Text displayed on the center of the entity. Updates cached surface as necessary."
  )

  def draw(this):
    surf = graphics.check()
    if surf:
      if this.fill == None:
        pg.draw.rect(surf, this.line, (this.x, this.y, this.w, this.h), this.thickness, this.round)
      else:
        pg.draw.rect(surf, this.fill, (this.x, this.y, this.w, this.h), 0, this.round)
      if this.__textsurf != None:
        graphics.blit_centered(this.__textsurf, this.x+this.w/2, this.y+this.h/2)