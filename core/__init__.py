import pygame
import math
import core.entity as entity
import core.graphics as graphics
from globals import *

player = entity.player_class()
screen = entity.entity("screen", 0, 0, 0, 1, "aabb")
screen.w = 99999
screen.h = 99999

def addEnemy(var, x, y, radius = 32):
  if var == "base":
    entities.append(entity.enemy("base", x, y, 90, radius))

def load():
  # Load the game here
  surf = pygame.display.get_surface()
  screen.w = surf.get_width()
  screen.h = surf.get_height()

  # Player may have custom load operations
  player.load()

  # Load sprites
  images["bullet_base"] = pygame.image.load("assets\image\projectile\\bullet_base.png")
  images["enemy_base"] = pygame.image.load("assets\image\enemy\enemy_base.png")

def update(dt):
  # Update game state

  # Ensure screen object is up to date
  screen.w = pygame.display.get_surface().get_width()
  screen.h = pygame.display.get_surface().get_height()

  # Player is separate from entities
  player.update(dt)
  if keyIsDown("up"):
    player.forward(player.speed * dt)
  if keyIsDown("down"):
    player.backward(player.speed * dt)
  if keyIsDown("left"):
    player.left(player.speed * dt)
  if keyIsDown("right"):
    player.right(player.speed * dt)
  # Clamp player specifically to screen bounds
  player.x = clamp(player.x, 0, screen.w)
  player.y = clamp(player.y, 0, screen.h)

  # Update enemies and projectiles
  for bullet in bullets:
    bullet.update(dt)
    # Cull offscreen
    bullet.alive = bullet.alive and bullet.intersects(screen)
  for entity in entities:
    entity.update(dt)
    # Cull offscreen
    entity.alive = bullet.alive and entity.intersects(screen)
    if entity.alive and entity.intersects(player):
      player.damage(entity.health)
      entity.health = 0
  
  # Handle collisions
  for bullet in bullets:
    for entity in entities:
      if bullet.intersects(entity):
        bullet.impact(entity)

  # Remove dead entities
  vEntity = None
  for i in range(len(entities) - 1, -1, -1):
    vEntity = entities[i]
    if vEntity.health <= 0:
      vEntity.delete()
    if not vEntity.alive:
      entities.pop(i)
  
  # Remove dead bullets
  vBullet = None
  for i in range(len(bullets) - 1, -1, -1):
    vBullet = bullets[i]
    if not vBullet.alive:
      bullets.pop(i)

def draw():
  # Initially proposed as script code.
  # Bullets drawn before entities in order to appear "below."
  for bullet in bullets:
    bullet.draw()
  for entity in entities:
    entity.draw()
  player.draw()

# Input helper
keys = {
  "\b": pygame.K_BACKSPACE,
  "\t": pygame.K_TAB,
  "clear": pygame.K_CLEAR, # Likely not accessible
  "\r": pygame.K_RETURN, # Actual keycode in ASCII
  "\n": pygame.K_RETURN, # Alternate format for usability
  "return": pygame.K_RETURN, # Alternate format for usability
  "enter": pygame.K_RETURN, # Alternate format for usability
  "pause": pygame.K_PAUSE, # May only be available when keyboard is grabbed
  "esc": pygame.K_ESCAPE, # Alternate format for usability
  "^[": pygame.K_ESCAPE, # Actual keycode in ASCII
  "space": pygame.K_SPACE, # Alternate format for usability
  " ": pygame.K_SPACE, # Actual keycode in ASCII
  "!": pygame.K_EXCLAIM,
  "\"": pygame.K_QUOTEDBL,
  "#": pygame.K_HASH,
  "$": pygame.K_DOLLAR,
  "&": pygame.K_AMPERSAND,
  "'": pygame.K_QUOTE,
  "(": pygame.K_LEFTPAREN,
  ")": pygame.K_RIGHTPAREN,
  "*": pygame.K_ASTERISK,
  "+": pygame.K_PLUS,
  ",": pygame.K_COMMA,
  "-": pygame.K_MINUS,
  ".": pygame.K_PERIOD,
  "/": pygame.K_SLASH,
  "0": pygame.K_0,
  "1": pygame.K_1,
  "2": pygame.K_2,
  "3": pygame.K_3,
  "4": pygame.K_4,
  "5": pygame.K_5,
  "6": pygame.K_6,
  "7": pygame.K_7,
  "8": pygame.K_8,
  "9": pygame.K_9,
  ":": pygame.K_COLON,
  ";": pygame.K_SEMICOLON,
  "<": pygame.K_LESS,
  "=": pygame.K_EQUALS,
  ">": pygame.K_GREATER,
  "?": pygame.K_QUESTION,
  "@": pygame.K_AT,
  "[": pygame.K_LEFTBRACKET,
  "\\": pygame.K_BACKSLASH,
  "]": pygame.K_RIGHTBRACKET,
  "^": pygame.K_CARET,
  "_": pygame.K_UNDERSCORE,
  # Lowercase
  "a": pygame.K_a,
  "b": pygame.K_b,
  "c": pygame.K_c,
  "d": pygame.K_d,
  "e": pygame.K_e,
  "f": pygame.K_f,
  "g": pygame.K_g,
  "h": pygame.K_h,
  "i": pygame.K_i,
  "j": pygame.K_j,
  "k": pygame.K_k,
  "l": pygame.K_l,
  "m": pygame.K_m,
  "n": pygame.K_n,
  "o": pygame.K_o,
  "p": pygame.K_p,
  "q": pygame.K_q,
  "r": pygame.K_r,
  "s": pygame.K_s,
  "t": pygame.K_t,
  "u": pygame.K_u,
  "v": pygame.K_v,
  "w": pygame.K_w,
  "x": pygame.K_x,
  "y": pygame.K_y,
  "z": pygame.K_z,
  # Capitals
  "A": pygame.K_a,
  "B": pygame.K_b,
  "C": pygame.K_c,
  "D": pygame.K_d,
  "E": pygame.K_e,
  "F": pygame.K_f,
  "G": pygame.K_g,
  "H": pygame.K_h,
  "I": pygame.K_i,
  "J": pygame.K_j,
  "K": pygame.K_k,
  "L": pygame.K_l,
  "M": pygame.K_m,
  "N": pygame.K_n,
  "O": pygame.K_o,
  "P": pygame.K_p,
  "Q": pygame.K_q,
  "R": pygame.K_r,
  "S": pygame.K_s,
  "T": pygame.K_t,
  "U": pygame.K_u,
  "V": pygame.K_v,
  "W": pygame.K_w,
  "X": pygame.K_x,
  "Y": pygame.K_y,
  "Z": pygame.K_z,
  "del": pygame.K_DELETE,
  "kp0": pygame.K_KP0,
  "kp1": pygame.K_KP1,
  "kp2": pygame.K_KP2,
  "kp3": pygame.K_KP3,
  "kp4": pygame.K_KP4,
  "kp5": pygame.K_KP5,
  "kp6": pygame.K_KP6,
  "kp7": pygame.K_KP7,
  "kp8": pygame.K_KP8,
  "kp9": pygame.K_KP9,
  "kp.": pygame.K_KP_PERIOD,
  "kp/": pygame.K_KP_DIVIDE,
  "kp*": pygame.K_KP_MULTIPLY,
  "kpenter": pygame.K_KP_ENTER,
  "kp=": pygame.K_KP_ENTER,
  "up": pygame.K_UP,
  "down": pygame.K_DOWN,
  "left": pygame.K_LEFT,
  "right": pygame.K_RIGHT,
  "ins": pygame.K_INSERT,
  "insert": pygame.K_INSERT,
  "home": pygame.K_HOME,
  "end": pygame.K_END,
  "pgup": pygame.K_PAGEUP,
  "PgUp": pygame.K_PAGEUP,
  "pgdn": pygame.K_PAGEDOWN,
  "PgDn": pygame.K_PAGEDOWN
}

def keyIsDown(key):
  state = pygame.key.get_pressed()
  if isinstance(key, str):
    if not (key in keys):
      return False
    return state[keys[key]]
  return state[key]

def keydown(key, mod, unicode, scancode):
  # Handle key presses

  # Simple main fire operation
  if key == pygame.K_SPACE:
    player.fire()

def keyup(key, mod, unicode, scancode):
  # Handle key releases
  pass

def mousedown(button, x, y):
  # Handle mouse button presses
  pass

def mouseup(button, x, y):
  # Handle mouse button releases
  pass

# Miscellaneous helpers for kids

# Simple clamp function.
# Returns v restricted to the range [a, b] (inclusive)
def clamp(v, a, b):
  if v < a: return a
  if v > b: return b
  return v

# Clamps to the current horizontal dimensions of the game window.
def clampX(x):
  return clamp(x, screen.x, screen.w)
# Clamps to the current vertical dimensions of the game window.
def clampY(y):
  return clamp(y, screen.y, screen.h)
