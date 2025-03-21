import pygame
import math
from core import util
from core.graphics import main as graphics_main
from core.globals import images

class image():
  default = None
  animStyles = {
    "none": "none",
    "single": "single",
    "loop": "loop"
  }
  __metareg = {}

  def __init__(this, img: pygame.surface.Surface, frames_x = 1, frames_y = 1, duration = 1):
    if isinstance(img, str):
      img = pygame.image.load(img)
    this.img = img
    image.__metareg[img] = this
    if frames_x > 1 or frames_y > 1:
      this.frames = []
      this.slice(frames_x, frames_y, duration, "loop")
    else:
      this.animated = False
      this.animStyle = "none"
      this.frames = [(0, 0, img.get_width(), img.get_height())]
      this.duration = 1
    this.__transform_cache = {}
  
  def copy(this):
    ret = image(this.img.copy())
    ret.animated = this.animated
    ret.animStyle = this.animStyle
    ret.frames = this.frames.copy()
    ret.duration = this.duration
    return ret

  def slice(this, frames_x, frames_y, duration = None, animStyle = "loop"):
    this.frames.clear()
    w = this.img.get_width()
    h = this.img.get_height()
    for y in range(0, frames_y):
      for x in range(0, frames_x):
        this.frames.append((x*w/frames_x, y*h/frames_y, w/frames_x, h/frames_y))
    this.w = w / frames_x
    this.h = h / frames_y
    this.animated = True
    if duration != None:
      this.duration = duration
    this.animStyle = animStyle
    return this
  
  def getmeta(img):
    if img in image.__metareg:
      return image.__metareg[img]
    else:
      return image.default
  
  def getFrameIndex(this, t = 0):
    if this.animated:
      baseframe = math.floor((t/this.duration) * len(this.frames))
      if this.animStyle == "single":
        return util.clamp(baseframe, 0, len(this.frames)-1)
      elif this.animStyle == "loop":
        return baseframe%len(this.frames)
      else:
        return baseframe
    return 0
      
  def getFrame(this, t = 0):
    i = this.getFrameIndex(t)
    return this.frames[i]
  
  def load_core(path, name, frames_x = 1, frames_y = 1, length = 1):
    img = pygame.image.load("assets\image\\" + path + "\\" + name + ".png")
    ret = image(img, frames_x, frames_y, length)
    images[name] = ret
    return ret
  
  def load(path, frames_x = 1, frames_y = 1, length = 1):
    img = pygame.image.load(path)
    ret = image(img, frames_x, frames_y, length)
    return ret
  
  # Rotozooms all frames individually and assembles them into a row on a new sprite sheet.
  # This sprite sheet and the frame definitions replace the current ones, use rotozoom() to create a new image.
  def rotozoom_self(this, angle = 0, scale = 1):
    totalwidth = 0
    maxheight = 0
    tempframes = []
    frame = None
    # Rotozoom all frames individually
    for framebounds in this.frames:
      frame = this.img.subsurface(framebounds)
      frame = pygame.transform.rotozoom(frame, -angle, scale)
      tempframes.append(frame)
      totalwidth += frame.get_width()
      if frame.get_height() > maxheight:
        maxheight = frame.get_height()
    # Set up new source image (surf) and frame divisions
    surf = pygame.surface.Surface((totalwidth, maxheight), pygame.SRCALPHA, this.img)
    x = 0
    this.frames.clear()
    for frame in tempframes:
      surf.blit(frame, (x, 0))
      this.frames.append((x, 0, frame.get_width(), frame.get_height()))
      x += frame.get_width()
    this.img = surf
    return this
  
  # Rotates and zooms all frames separately, then assembles them into a new image object.
  # Automatically caches rotations of parent images.
  # Best used by just sending the properties dynamically through draw()
  # TODO: dispose unused image rotations
  def rotozoom(this, angle = 0, scale = 1):
    snapped_angle = round(angle%360, -1)
    if snapped_angle in this.__transform_cache:
      anglecache = this.__transform_cache[snapped_angle]
      if scale in anglecache:
        return anglecache[scale]
      else:
        ret = this.copy().rotozoom_self(angle, scale)
        anglecache[scale] = ret
        return ret
    else:
      anglecache = {}
      this.__transform_cache[snapped_angle] = anglecache
      ret = this.copy().rotozoom_self(snapped_angle, scale)
      anglecache[scale] = ret
      return ret

  # Draws this image onto the current target surface. If scale or angle are not default,
  # creates (and returns) a new image object rotozoomed appropriately.
  def draw(this, t = 0, x = 0, y = 0, scale = 1, angle = 0, flags = 0):
    surf = graphics_main.check()
    if surf == None:
      return
    if scale == 1 and angle == 0:
      surf.blit(this.img, (x, y), this.getFrame(t), flags)
      return this
    else:
      newimg = this.rotozoom(angle, scale)
      return newimg.draw(t, x, y, flags)
  
  def draw_centered(this, t = 0, x = 0, y = 0, scale = 1, angle = 0, flags = 0):
    surf = graphics_main.check()
    if surf == None:
      return
    if scale == 1 and angle == 0:
      dims = this.getFrame(t)
      dx = dims[2]/2
      dy = dims[3]/2
      surf.blit(this.img, (x-dx, y-dy), dims, flags)
      return this
    else:
      newimg = this.rotozoom(angle, scale)
      return newimg.draw_centered(t, x, y, 1, 0, flags)
  
  def get_width(this):
    w = 0
    for frame in this.frames:
      w = max(frame[2], w)
    return w
  
  def get_height(this):
    h = 0
    for frame in this.frames:
      h = max(frame[3], h)
    return h
