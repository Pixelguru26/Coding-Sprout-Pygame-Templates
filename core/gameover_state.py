import pygame as pg
from core import setState
import core.module_uilib as uilib

uiroot = uilib.uielement(0, 0, 0, 0)
class __colorset(): pass
colorset = __colorset()
colorset.nicegreen = (25, 128, 64, 255)
colorset.nicegreen_bright = (48, 220, 80, 255)
colorset.darkgreen = (0, 50, 0, 255)

def __onclick_restart(this, x, y, b):
  setState("menu")

def load():
  (w, h) = pg.display.get_surface().get_size()
  uiroot.style.filled = False
  uibody = uilib.splitpane(0, 0, w, h)
  uibody.dynw = 1
  uibody.dynh = 1
  uiroot.addchild(uibody)
  uibody.addchild(uilib.uielement(0, 0, 0, 0))
  uilist = uilib.uielement(0, 0, w/3, h)
  uibody.addchild(uilist)
  uibody.addchild(uilib.uielement(0, 0, 0, 0))
  title = uilib.uielement(0, h/3, 300, 75)
  title.text = "GAME OVER"
  title.dynmx = 0.5
  uilist.addchild(title)
  uirestart = uilib.uielement(0, 2*h/3, 300, 75)
  uirestart.dynmx = 0.5
  uirestart.style.filled = True
  uirestart.style.fill = colorset.nicegreen
  uirestart.style.text = colorset.darkgreen
  uirestart.text = "Restart"
  def onhover_glow(this, x, y, dx, dy):
    uirestart.style.fill = colorset.nicegreen_bright
  uirestart.onhoverin = onhover_glow
  def onhoverout_darken(this, x, y, dx, dy):
    uirestart.style.fill = colorset.nicegreen
  uirestart.onhoverout = onhoverout_darken
  uirestart.onclick = __onclick_restart
  uilist.addchild(uirestart)

def update(dt):
  uiroot.w = pg.display.get_surface().get_width()
  uiroot.h = pg.display.get_surface().get_height()
  uiroot.children[0].w = uiroot.w
  uiroot.children[0].h = uiroot.h
  uiroot.internal_update(dt)

def draw():
  uiroot.force_redraw()

def keydown(key, mod, unicode, scancode):
  uiroot.internal_keyevt(key, mod, unicode, scancode, "onkeydown")

def keyup(key, mod, unicode, scancode):
  uiroot.internal_keyevt(key, mod, unicode, scancode, "onkeyup")

def mousedown(mouse_button, x, y):
  uiroot.internal_mouseclickevt(x, y, mouse_button, "onclick")

def mouseup(mouse_button, x, y):
  uiroot.internal_mouseclickevt(x, y, mouse_button, "onclickrelease")

def mousemotion(x, y, dx, dy, buttons):
  uiroot.internal_mousemovevt(x, y, dx, dy, "onmousemoved")

def mousewheel(x, y):
  (mx, my) = pg.mouse.get_pos()
  uiroot.internal_mousemovevt(mx, my, x, y, "onscroll")