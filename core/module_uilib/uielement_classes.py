import core.geometry as geo
import core.graphics as gfx
from core.module_uilib.style_class import uistyle
import pygame as pg
import types

class __uicolors: pass
uicolors = __uicolors()
uicolors.nicegreen = (25, 128, 64, 255)
uicolors.nicegreen_bright = (48, 220, 80, 255)
uicolors.darkgreen = (0, 50, 0, 255)

def callmethod(entity, key, *arg):
  if hasattr(entity, key):
    method = getattr(entity, key)
    if isinstance(method, types.MethodType):
      if len(arg) < 1:
        return method()
      else:
        return method(*arg)
    elif isinstance(method, types.FunctionType):
      if len(arg) < 1:
        return method(entity)
      else:
        return method(entity, *arg)
      

class uielement():
  __lastid = -1
  def __init__(this, x, y, w, h, style = None):
    uielement.__lastid += 1
    this.id = uielement.__lastid
    this.__x = x
    this.__y = y
    this.__w = w
    this.__h = h
    # Dynamic dimensions
    # These are multipliers of parent dimensions if not None and if parent allows.
    # When used, these recalculate the appropriate actual dimensions as needed.
    this.dynx = None
    this.dyny = None
    this.dynw = None
    this.dynh = None
    # Used for centered locations, replaces dynx and dyny if set.
    this.dynmx = None
    this.dynmy = None
    # These apply to children.
    # Individual dynamic dimensions override main general disable if true.
    this.enabledyn = True
    this.enabledynx = False
    this.enabledyny = False
    this.enabledynw = False
    this.enabledynh = False
    this.parent = None
    this.children = []
    if style == None:
      this.style = uistyle()
    else:
      this.style = style
    # Not yet implemented
    # this.__surface = pg.surface.Surface((this.w + this.style.linewidth, this.h + this.style.linewidth), pg.SRCALPHA, 32)
    # this.__surface.fill((0, 0, 0, 0))
    this.__text = ""
    this.cached_textsurf = None
    this.dirty = True
    this.layoutDirty = True
    this.hovered = False
  
  def __eq__(this, value: object) -> bool:
    return isinstance(value, uielement) and value.id == this.id

  def internal_set_text(this, txt):
    if txt != this.__text:
      this.__text = txt
      this.cached_textsurf = this.style.font.render(this.__text, True, this.style.text)
      this.dirty = True
  
  text = property(
    fget=lambda this : this.__text,
    fset=internal_set_text,
    fdel=lambda this : delattr(this, "__text"),
    doc="Text to be displayed in the ui element"
  )

  def __set_x(this, val):
    if this.__x == val: return
    this.dirty = True
    this.layoutDirty = True
    this.__x = val

  x = property(
    fget=lambda this : this.__x,
    fset=__set_x,
    fdel = lambda this : delattr(this, "__x"),
    doc="Left x position"
  )

  def __set_y(this, val):
    if this.__y == val: return
    this.dirty = True
    this.layoutDirty = True
    this.__y = val

  y = property(
    fget=lambda this : this.__y,
    fset=__set_y,
    fdel=lambda this : delattr(this, "__y"),
    doc="Top y position"
  )

  def __set_w(this, val):
    if this.__w == val: return
    this.dirty = True
    this.layoutDirty = True
    this.__w = val
  
  w = property(
    fget=lambda this : this.__w,
    fset=__set_w,
    fdel=lambda this : delattr(this, "__w"),
    doc="Width in pixels"
  )

  def __set_h(this, val):
    if this.__h == val: return
    this.dirty = True
    this.layoutDirty = True
    this.__h = val
  
  h = property(
    fget=lambda this : this.__h,
    fset=__set_h,
    fdel=lambda this : delattr(this, "__h"),
    doc="Height in pixels"
  )

  def __set_mx(this, val):
    this.x = val - this.w/2
  
  def __set_my(this, val):
    this.y = val - this.h/2
  
  mx = property(
    fget=lambda this : this.__x + this.__w/2,
    fset=__set_mx,
    fdel=lambda a : a,
    doc="middle x position"
  )

  my = property(
    fget=lambda this : this.__y + this.__h/2,
    fset=__set_my,
    fdel=lambda a : a,
    doc="middle y position"
  )
  
  def intersect(this, other):
    return geo.intersect_aabb(this.__x, this.__y, this.w, this.h, other.x, other.y, other.w, other.h)
  
  def drawfill(this, parent = None, offsetx = 0, offsety = 0):
    surf = gfx.check()
    if surf != None and this.style.filled:
      pg.draw.rect(surf, this.style.fill, (this.__x + offsetx, this.__y + offsety, this.w, this.h), 0, this.style.radius)

  def drawline(this, parent = None, offsetx = 0, offsety = 0):
    surf = gfx.check()
    if surf != None and this.style.linewidth != 0:
      pg.draw.rect(surf, this.style.line, (this.__x + offsetx, this.__y + offsety, this.w, this.h), this.style.linewidth, this.style.radius)

  def drawtext(this, parent = None, offsetx = 0, offsety = 0):
    surf = gfx.check()
    if surf != None and this.__text != "":
      cx = this.__x + offsetx + this.w/2
      cy = this.__y + offsety + this.h/2
      # this.__textsurf = this.style.font.render(this.__text, True, this.style.text)
      surf.blit(this.cached_textsurf, (cx - this.cached_textsurf.get_width()/2, cy-this.cached_textsurf.get_height()/2))

  def redraw(this, parent = None, offsetx = 0, offsety = 0):
    this.drawfill(parent, offsetx, offsety)
    this.drawline(parent, offsetx, offsety)
    this.drawtext(parent, offsetx, offsety)
    this.dirty = False

  def stylebounds(this, offsetx = 0, offsety = 0):
    return this.style.getbounds(this.__x + offsetx, this.__y + offsety, this.w, this.h)

  def redraw_if_dirty(this, parent = None, offsetx = 0, offsety = 0):
    if this.layoutDirty:
      this.internal_update_layout(parent, offsetx, offsety)
    surf = gfx.check()
    clip = surf.get_clip()
    if this.dirty:
      callmethod(this, "redraw", offsetx, offsety)
    surf.set_clip(clip.clip(this.stylebounds(offsetx, offsety)))
    for child in this.children:
      child.redraw_if_dirty(this, offsetx + this.x, offsety + this.y)
    surf.set_clip(clip)

  def force_redraw(this, parent = None, offsetx = 0, offsety = 0):
    if this.layoutDirty:
      this.internal_update_layout(parent, offsetx, offsety)
    surf = gfx.check()
    clip = surf.get_clip()
    callmethod(this, "redraw", parent, offsetx, offsety)
    surf.set_clip(clip.clip(this.stylebounds(offsetx, offsety)))
    for child in this.children:
      child.force_redraw(this, offsetx + this.x, offsety + this.y)
    surf.set_clip(clip)
  
  def internal_mousemovevt(this, x, y, dx, dy, evt):
    allowThrough = True
    posthover = x >= this.x and x <= this.x+this.w and y >= this.y and y <= this.y+this.h
    prehover = (x-dx) >= this.x and (x-dx) <= this.x+this.w and (y-dy) >= this.y and (y-dy) <= this.y+this.h
    if posthover or prehover:
      if evt == "onmousemoved":
        if posthover:
          if prehover:
            evt = "onmousemoved"
          else:
            evt = "onhoverin"
            this.hovered = True
        elif prehover:
          evt = "onhoverout"
          this.hovered = False
      for child in this.children:
        allowThrough = allowThrough and child.internal_mousemovevt(x-this.__x, y-this.__y, dx-this.__x, dy-this.__y, evt)
        if not allowThrough:
          break
      if allowThrough and hasattr(this, evt):
        return callmethod(this, evt, x-this.__x, y-this.__y, dx, dy)
    elif this.hovered:
      this.hovered = False
      for child in this.children:
        allowThrough = allowThrough and child.internal_mousemovevt(x-this.__x, y-this.__y, dx-this.__x, dy-this.__y, "onhoverout")
        if not allowThrough:
          break
      if allowThrough and hasattr(this, "onhoverout"):
        return callmethod(this, "onhoverout", x-this.__x, y-this.__y, dx, dy)
    return allowThrough
  
  def internal_mouseclickevt(this, x, y, button, evt):
    allowThrough = True
    if x >= this.x and x <= this.x+this.w and y >= this.y and y <= this.y+this.h:
      for child in this.children:
        allowThrough = allowThrough and child.internal_mouseclickevt(x-this.__x, y-this.__y, button, evt)
        if not allowThrough: break
      if allowThrough and hasattr(this, evt):
        return callmethod(this, evt, x, y, button)
    return allowThrough
  
  def internal_update(this, dt):
    callmethod(this, "update", dt)
    for child in this.children:
      child.internal_update(dt)
  
  def internal_keyevt(this, key, mod, unicode, scancode, evt):
    callmethod(this, evt, key, mod, unicode, scancode)
    for child in this.children:
      child.internal_keyevt(key, mod, unicode, scancode, evt)
  
  def addchild(this, child):
    this.children.append(child)
    child.parent = this
    this.dirty = True
    return child
  
  # alignments = {
  #   "top": {
  #     "left": 0,
  #     "middle": 1,
  #     "right": 2
  #   },
  #   "middle": {
  #     "left": 3,
  #     "middle": 4,
  #     "right": 5
  #   },
  #   "bottom": {
  #     "left": 6,
  #     "middle": 7,
  #     "right": 8
  #   }
  # }

  def dynlayout_child(this, child, w = None, h = None):
    if w == None:
      w = this.w
    if h == None:
      h = this.h
    if this.enabledyn or this.enabledynx:
      if child.dynmx != None:
        child.mx = w * child.dynmx
      elif child.dynx != None:
        child.x = w * child.dynx
    if this.enabledyn or this.enabledyny:
      if child.dynmy != None:
        child.my = h * child.dynmy
      elif child.dyny != None:
        child.y = h * child.dyny
    if this.enabledyn or this.enabledynw:
      if child.dynw != None:
        child.w = w * child.dynw
    if this.enabledyn or this.enabledynh:
      if child.dynh != None:
        child.h = h * child.dynh

  def dynlayout_all(this, w = None, h = None):
    for child in this.children:
      this.dynlayout_child(child, w, h)
  
  def internal_update_layout(this, parent = None, offsetx = 0, offsety = 0):
    # If element is root, screen is used as parent and assumed to allow dynamic dims.
    if parent == None:
      surf = pg.display.get_surface()
      if this.dynx != None:
        this.x = surf.get_width() * this.dynx
      if this.dyny != None:
        this.y = surf.get_height() * this.dyny
      if this.dynw != None:
        this.w = surf.get_width() * this.dynw
      if this.dynh != None:
        this.h = surf.get_height() * this.dynh
    if hasattr(this, "update_layout"):
      callmethod(this, "update_layout", parent, offsetx, offsety)
    else:
      this.dynlayout_all()
    for child in this.children:
      child.internal_update_layout(this, offsetx + this.x, offsety + this.y)
    this.layoutDirty = False

class splitpane(uielement):
  def __init__(this, x, y, w, h, vertical = False, style=None):
    uielement.__init__(this, x, y, w, h, style)
    this.enabledyn = False
    if vertical:
      this.orientation = "vertical"
      this.enabledynx = True
    else:
      this.orientation = "horizontal"
      this.enabledyny = True
    this.enabledynw = True
    this.enabledynh = True
  
def __splitpane_update_layout(this, parent = None, offsetx = 0, offsety = 0):
  x = 0
  y = 0
  if this.orientation == "vertical":
    subheight = this.h/len(this.children)
    for child in this.children:
      this.dynlayout_child(child, this.w, subheight)
      child.my = y + subheight/2
      child.mx = this.w/2
      y += subheight
  else:
    subwidth = this.w/len(this.children)
    for child in this.children:
      this.dynlayout_child(child, subwidth, this.h)
      child.mx = x + subwidth/2
      child.my = this.h/2
      x += subwidth
splitpane.update_layout = __splitpane_update_layout

class progressbar(uielement):
  def __init__(this, x, y, w, h, color=(255, 255, 255, 255), style=None):
    uielement.__init__(this, x, y, w, h, style)
    this.__progress = 0
    this.color = color
  
  def __set_progress(this, val):
    val = min(max(val, 0), 1)
    if val != this.__progress:
      this.__progress = val
      this.dirty = True
  
  progress = property(
    fget=lambda this : this.__progress,
    fset=__set_progress,
    fdel=lambda this : delattr(this, "__progress"),
    doc="The indicated value for the bar, in range 0 to 1."
  )

  def redraw(this, parent = None, offsetx = 0, offsety = 0):
    x = this.x + offsetx
    y = this.y + offsety
    surf = gfx.check()
    if surf == None:
      return
    this.drawfill(parent, offsetx, offsety)
    pg.draw.rect(surf, this.color, (x, y, this.w * this.__progress, this.h), 0, -1, this.style.radius, -1, this.style.radius, -1)
    this.drawtext(parent, offsetx, offsety)
    this.drawline(parent, offsetx, offsety)
    this.dirty = False

class textelement(uielement):
  def __init__(this, cx, cy, text, fontsize = 20):
    style = uistyle()
    style.font = pg.font.Font(None, fontsize)
    style.font.set_bold(True)
    uielement.__init__(this, 0, 0, 0, 0, style)
    this.text = text
    this.x = cx-this.cached_textsurf.get_width()/2
    this.y = cy-this.cached_textsurf.get_width()
    this.w = this.cached_textsurf.get_width()
    this.h = this.cached_textsurf.get_height()

class verticallistelement(uielement):
  def __init__(this, x, y, w, h, style=None):
    uielement.__init__(this, x, y, w, h, style)
    this.scroll = 0
    this.drawque = []
    this.enabledyn = False
    this.enabledynx = True
    this.enabledynw = True
    this.enabledynh = True

  def update_layout(this, parent = None, offsetx = 0, offsety = 0):
    y = -this.scroll
    surf = gfx.check()
    if surf == None:
      return
    oldclip = surf.get_clip()
    surf.set_clip(oldclip.clip(this.stylebounds(offsetx, offsety)))
    
    this.drawque.clear()
    for child in this.children:
      child.y = y
      y += child.h
      if child.y <= this.h and child.y+child.h > 0:
        this.drawque.append(child)
  
  def onscroll(this, x, y, dx, dy):
    this.scroll += dy

class numdisplayelement(textelement):
  def __init__(this, cx, cy, title, readlambda, fontsize=20):
    this.title = title
    this.readlambda = readlambda
    this.prev = readlambda()
    textelement.__init__(this, cx, cy, title + " : " + str(this.prev), fontsize)

  def update(this, dt):
    val = this.readlambda()
    if val != this.prev:
      this.prev = val
      this.text = this.title + " : " + str(val)

class menustackelement(uielement):
  def __init__(this, x, y, w, h, style=None):
    uielement.__init__(this, x, y, w, h, style)
    this.gap = 10
    this.orientation = "topdown"
  
  def update_layout(this, parent = None, offsetx = 0, offsety = 0):
    if this.orientation == "topdown":
      y = 0
      for child in this.children:
        child.mx = this.w/2
        child.y = y
        this.dynlayout_child(child, this.w, this.h - y)
        if child.dynmy != None or child.dyny != None:
          child.y += y
        y = child.y + child.h + this.gap

class simplebuttonelement(uielement):
  def __init__(this, x, y, w, h, text):
    uielement.__init__(this, x, y, w, h)
    this.dynmx = 0.5
    this.dynmy = 0.5
    this.style.filled = True
    this.basecolor = uicolors.nicegreen
    this.highlight = uicolors.nicegreen_bright
    this.textcolor = uicolors.darkgreen
    this.style.fill = this.basecolor
    this.style.text = this.textcolor
    this.text = text
  
  def onhoverin(this, x, y, dx, dy):
    this.style.fill = this.highlight
    this.dirty = True

  def onhoverout(this, x, y, dx, dy):
    this.style.fill = this.basecolor
    this.dirty = True