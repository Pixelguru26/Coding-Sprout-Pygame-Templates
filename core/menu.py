
import pygame
import pygame.font
import pygame.draw
from core.graphics import check
from core import setState

buttons = []
default_font = None

class button:
  def __init__(this, x, y, w, h, text, onclick):
    this.x = x
    this.y = y
    this.w = w
    this.h = h
    this.text = text
    this.color = (50, 255, 128, 100)
    this.onclick = onclick
    this.__hovered = False
    this.__clickdown = False
    this.update_graphics()
  
  def update_graphics(this):
    global default_font
    this.__text_cache = default_font.render(this.text, True, (0, 50, 0, 255))
    this.__box_cache = pygame.surface.Surface((this.w, this.h))
    this.update_color()

  def update_color(this, color = None):
    if color != None:
      this.color = color
    this.__box_cache.fill(this.color)
    this.__box_cache.set_alpha(this.color[3])

  def draw(this):
    surface = check()
    surface.blit(this.__box_cache, (this.x, this.y))
    centerx = this.x + this.w/2
    centery = this.y + this.h/2
    text_offset_x = this.__text_cache.get_width()/2
    text_offset_y = this.__text_cache.get_height()/2
    surface.blit(this.__text_cache, (centerx - text_offset_x, centery - text_offset_y))
    
  def update(this, dt):
    mx, my = pygame.mouse.get_pos()
    if this.test(mx, my):
      if not this.__hovered:
        this.__hovered = True
        this.onhover()
    else:
      if this.__clickdown:
        this.__clickdown = False
        this.onclickup(None, mx, my)
      if this.__hovered:
        this.__hovered = False
        this.onhoverout()

  def onhover(this):
    this.__base_color = this.color
    this.update_color((50, 255, 100, 200))

  def onhoverout(this):
    this.update_color(this.__base_color)

  def onclickdown(this, b, x, y):
    this.__clickdown = True
    this.onclick(this, b, x, y)
  
  def onclickup(this, b, x, y):
    pass

  def test(this, x, y):
    return x >= this.x and x <= this.x + this.w and y >= this.y and y <= this.y + this.h
  
  def testclick(this, b, x, y):
    if this.test(x, y):
      this.onclickdown(b, x, y)
  
  def testrelease(this, b, x, y):
    if this.__clickdown:
      this.__clickdown = False
      this.onclickup(b, x, y)

def load():
  global default_font
  default_font = pygame.font.Font(None, 32)
  default_font.set_bold(True)
  buttons.clear()

  # Instantiate buttons and menu
  buttons.append(button(10, 10, 300, 75, "Play", lambda this, b, x, y: setState("game")))

def update(dt):
  for button in buttons:
    button.update(dt)

def draw():
  for button in buttons:
    button.draw()

def keydown(key, mod, unicode, scancode):
  pass

def keyup(key, mod, unicode, scancode):
  pass

def mousedown(mouse_button, x, y):
  for v_button in buttons:
    v_button.testclick(mouse_button, x, y)

def mouseup(mouse_button, x, y):
  for v_button in buttons:
    v_button.testrelease(mouse_button, x, y)
