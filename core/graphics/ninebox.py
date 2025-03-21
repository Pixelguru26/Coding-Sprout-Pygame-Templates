from math import floor, ceil
from pygame.rect import Rect as rect
import pygame.draw
import core.graphics.main as __g

# Unfinished
class ninebox:
  def __init__(this, img, color, x1, y1, x2, y2):
    this.regions = []
    this.recalc(img, color, x1, y1, x2, y2)
  
  def recalc(this, img=None, color=None, x1=None, y1=None, x2=None, y2=None):
    if img != None:
      this.img = img
    if x1 != None:
      this.x1 = x1
    x1 = this.x1
    if y1 != None:
      this.y1 = y1
    y1 = this.y1
    if x2 != None:
      this.x2 = x2
    x2 = this.x2
    if y2 != None:
      this.y2 = y2
    y2 = this.y2
    if x1 < 1:
      x1 = floor(w*x1)
    if y1 < 1:
      y1 = floor(h*y1)
    if x2 <= 1:
      x2 = ceil(w*x2)
    if y2 <= 1:
      y2 = ceil(h*y2)
    (w, h) = this.img.get_size()
    this.regions[0] = rect(0, 0, x1, y1),
    this.regions[1] = rect(x1, 0, x2-x1, y1),
    this.regions[2] = rect(x2, 0, w-x2, y1),
    this.regions[3] = rect(0, y1, x1, y2-y1),
    if color != None:
      this.regions[4] = color,
    this.regions[5] = rect(x2, y1, w-x2, y2-y1),
    this.regions[6] = rect(0, y2, x1, h-y2),
    this.regions[7] = rect(x1, y2, x2-x1, h-y2),
    this.regions[8] = rect(x2, y2, w-x2, h-y2)

  def draw_outside(this, tgt, x, y, w, h, border_stretch=False):
    tgt.fill(this.regions[4], rect(x, y, w, h))
    border_top = this.img.subsurface(this.regions[1])
    border_left = this.img.subsurface(this.regions[3])
    border_right = this.img.subsurface(this.regions[5])
    border_bottom = this.img.subsurface(this.regions[7])
    if border_stretch:
      border_top = pygame.transform.scale(border_top, (w, border_top.get_height()))
      border_left = pygame.transform.scale(border_left, (border_left.get_width(), h))
      border_right = pygame.transform.scale(border_right, (border_right.get_width(), h))
      border_bottom = pygame.transform.scale(border_bottom, (w, border_bottom.get_height()))
      tgt.blit(border_top, (x, y-this.regions[1].h))
      tgt.blit(border_left, (x-this.regions[3].w, y))
      tgt.blit(border_right, (x+w, y))
      tgt.blit(border_bottom, (x, y+h))
    else:
      old_clip = tgt.get_clip()
      tgt.set_clip(rect(x, y-border_top.get_height(), w, h+border_top.get_height()+border_bottom.get_height()))
      for ix in range(x, x+w, border_top.get_width()):
        tgt.blit(border_top, (ix, y-border_top.get_height()))
      for ix in range(x, x+w, border_bottom.get_width()):
        tgt.blit(border_bottom, (ix, y+h))
      tgt.set_clip(rect(x-border_left.get_width(), y, w+border_left.get_width()+border_right.get_width(), h))
      for iy in range(y, y+h, border_left.get_height()):
        tgt.blit(border_left, (x-border_left.get_width(), iy))
      for iy in range(y, y+h, border_right.get_height()):
        tgt.blit(border_right, (x+w, iy))
      tgt.set_clip(old_clip)

    # Corners
    tgt.blit(this.img, (x-this.regions[0].w, y-this.regions[0].h), this.regions[0])
    tgt.blit(this.img, (x+w, y-this.regions[2].h), this.regions[2])
    tgt.blit(this.img, (x-this.regions[6].w, y+h), this.regions[6])
    tgt.blit(this.img, (x+w, y+h), this.regions[8])

  def draw(this, tgt, x, y, w, h, border_offset=0, border_stretch=False):
    tgt = __g.check()
    if tgt == None: return
    l = x - (border_offset+1)/2 * this.regions[0].w
    r = x+w + (border_offset-1)/2 * this.regions[2].w
    u = y - (border_offset+1)/2 * this.regions[0].h
    d = y+h + (border_offset-1)/2 * this.regions[6].h
    fx = x + (border_offset-1)/2 * this.regions[0].w
    fy = y + (border_offset-1)/2 * this.regions[0].h
    fx2 = x+w - (border_offset+1)/2 * this.regions[2].w
    fy2 = y+h - (border_offset+1)/2 * this.regions[6].h
    tgt.fill(this.regions[4], rect(fx, fy, fx2-fx, fy2-fy))
    tgt.blit(this.img, (l, u), this.regions[0])
    tgt.blit(this.img, (l+this.regions[0].w, u), this.regions[1])
    tgt.blit(this.img, (r, u), this.regions[2])
    tgt.blit(this.img, (l, u+this.regions[0].h), this.regions[3])
    tgt.blit(this.img, (r, u+this.regions[0].h), this.regions[5])
    tgt.blit(this.img, (l, d), this.regions[6])
    tgt.blit(this.img, (l+this.regions[0].w, d), this.regions[7])
    tgt.blit(this.img, (r, d), this.regions[8])
