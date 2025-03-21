import core.geometry as geo
import core.graphics as gfx
import pygame as pg

class uistyle():
  __default_font = None
  def __init__(this):
    this.fill = (0, 0, 0, 255)
    this.line = (255, 255, 255, 255)
    this.text = (255, 255, 255, 255)
    this.filled = False
    this.linewidth = 0
    this.radius = -1
    # For some unholy reason, default font may revert to none if assigned externally.
    if uistyle.__default_font == None:
      if not pg.font.get_init():
        pg.font.init()
      uistyle.__default_font = pg.font.Font(None, 32)
      uistyle.__default_font.set_bold(True)
    this.font = uistyle.__default_font
  
  def getbounds(this, x, y, w, h):
    if this.linewidth != 0:
      x -= this.linewidth/2
      y -= this.linewidth/2
      w += this.linewidth
      h += this.linewidth
    return (x, y, w, h)
