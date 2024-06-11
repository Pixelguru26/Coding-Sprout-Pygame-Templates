import math, pygame

class __libclass:
  pass
__lib = __libclass()
__lib.surface = None

def check():
  if __lib.surface == None:
    __lib.surface = pygame.display.get_surface()
  return __lib.surface

def blit(image, x, y):
  surf = check()
  if surf == None: return
  surf.blit(image, (x, y))

def blit_centered(image, x, y):
  surf = check()
  if surf == None: return
  cx = x - image.get_width()/2
  cy = y - image.get_height()/2
  surf.blit(image, (cx, cy))

# Produces a transformed image and draws it to the current surface on the fly, without caching.
# The transformed surface is returned after drawing.
def draw(image, x, y, scale = 1, angle = 0):
  # Ensure a surface exists to draw to
  surf = check()
  if surf == None: return
  # Pick an optimal level of transformation to avoid unnecessary work
  ret = None
  if angle != 0:
    ret = pygame.transform.rotozoom(image, -angle, scale)
  elif scale != 1:
    ret = pygame.transform.scale(image, scale)
  else:
    ret = image
  # Image finally rendered with center point at (x, y)
  x = x - ret.get_width()/2
  y = y - ret.get_height() / 2
  surf.blit(ret, (x, y))
  return ret
