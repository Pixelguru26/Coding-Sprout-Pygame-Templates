import core.globals as __g
import pygame.image as __pgimg
from core import GAME_DIR as __GAME_DIR
import os.path as __path
from math import floor as __floor
import core.util as __util

class animg:
  animstyles = {
    "loop": "loop",
    "single": "single",
    "pingpong": "pingpong",
    "still": "still",
    "dynamic": "dynamic"
  }

  def __init__(this, srcimg, framerate = 30, animstyle = "loop", x = 0, y = 0, w = -1, h = -1, spacex = 0, spacey = 0):
    if isinstance(srcimg, str):
      if srcimg in __g.images:
        srcimg = __g.images[srcimg]
      else:
        filepath = __GAME_DIR + "/assets/image/" + srcimg + ".png"
        if __path.isfile(filepath):
          __g.images[srcimg] = __pgimg.load(filepath)
          srcimg = __g.images[srcimg]
        else:
          print("Warning: could not load image [[" + filepath + "]], defaulting to error.")
          srcimg = __pgimg.load(__GAME_DIR+f"/assets/image/error.png")
    this.framerate = framerate
    this.animstyle = animstyle
    this.srcimg = srcimg
    this.frames = []
    if w < 0:
      w = srcimg.get_width()
    if h < 0 :
      h = srcimg.get_height()
    this.cut(x, y, w, h, spacex, spacey)

  def addframe(this, x, y, w, h):
    r = x + w
    d = y + h
    r = min(r, this.srcimg.get_width())
    d = min(d, this.srcimg.get_height())
    x = max(x, 0)
    y = max(y, 0)
    if r <= x:
      print("Null frame warning")
      return
    if d <= y:
      print("Null frame warning")
      return
    ret = (x, y, r-x, d-y)
    this.frames.append(ret)
    return ret
  
  def clear(this):
    this.frames.clear()

  def cut(this, x, y, w, h, spacex = 0, spacey = 0):
    cx = x
    cy = y
    while (cy < this.srcimg.get_height()):
      while (cx < this.srcimg.get_width()):
        this.addframe(cx, cy, w, h)
        cx += w+spacex
      cy += h+spacey

  def drawframe(this, surf, i, x, y, flags = 0):
    surf.blit(this.srcimg, (x, y), this.frames[i], flags)
  
  def drawframe_centered(this, surf, i, x, y, flags = 0):
    dx = -this.frames[i][2]/2
    dy = -this.frames[i][3]/2
    surf.blit_centered(this.srcimg, (x+dx, y+dy), this.frames[i], flags)
  
  def drawtime(this, surf, clock, x, y, flags = 0):
    surf.blit(this.srcimg, (x, y), this.frames[this.getframe(clock)], flags)

  def drawtime_centered(this, surf, clock, x, y, flags = 0):
    i = this.getframe(clock)
    dx = -this.frames[i][2]/2
    dy = -this.frames[i][3]/2
    surf.blit_centered(this.srcimg, (x+dx, y+dy), this.frames[i], flags)

  def getframe(this, clock):
    frame = __floor(this.framerate*clock)
    if this.animstyle == "loop":
      return frame%len(this.frames)
    elif this.animstyle == "single":
      return min(frame, len(this.frames)-1)
    elif this.animstyle == "pingpong":
      return __util.pingpong(frame, 0, len(this.frames)-1)
    elif this.animstyle == "still":
      return 0
    elif this.animstyle == "dynamic":
      return 0
    return frame

