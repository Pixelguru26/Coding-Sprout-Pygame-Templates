import sys, asyncio
sys.path.append('lib/python3.12/site-packages/core')

import pygame
from pygame.locals import *
import core

async def main():
  pygame.init()
  DISPLAYSURF = pygame.display.set_mode((1024, 800))
  pygame.display.set_caption('Hello World!')
  # frameClock = pygame.time.Clock()
  # Load game and user contributions
  core.__load()
  import game as script
  if "load" in dir(script):
    script.load()

  # Check for what's actually defined by the user
  script_kd = "keydown" in dir(script)
  script_ku = "keyup" in dir(script)
  script_md = "mousedown" in dir(script)
  script_mu = "mouseup" in dir(script)
  script_update = "update" in dir(script)
  script_draw = "draw" in dir(script)

  print("Begin execution")
  # Main event loop
  dt = 1/30 # Recent changes have prevented me from using proper delta time, so fixed loop it is I guess.
  while True: # All game end conditions currently break from the loop, so while true is safe.
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == KEYDOWN:
        if script_kd:
          script.keydown(event.key, event.mod, event.unicode, event.scancode)
        core.__keydown(event.key, event.mod, event.unicode, event.scancode)
      elif event.type == KEYUP:
        if script_ku:
          script.keyup(event.key, event.mod, event.unicode, event.scancode)
        core.__keyup(event.key, event.mod, event.unicode, event.scancode)
      elif event.type == MOUSEBUTTONDOWN:
        if script_md:
          script.mousedown(event.button, event.pos[0], event.pos[1])
        core.__mousedown(event.button, event.pos[0], event.pos[1])
      elif event.type == MOUSEBUTTONUP:
        if script_mu:
          script.mouseup(event.button, event.pos[0], event.pos[1])
        core.__mouseup(event.button, event.pos[0], event.pos[1])
    # Update and delta time calculations
    # These break in the HTML version
      # frameClock.tick(1000) # Ensure a maximum tick rate to prevent stalling at high fps
      # dt = frameClock.get_time() / 1000 # Pygame's clock measures in milliseconds
    await asyncio.sleep(1/60)
    if script_update:
      script.update(dt)
    core.__update(dt)

    # Rendering
    if core.settings["clearscreen"]:
      DISPLAYSURF.fill((0, 0, 0))
    core.__draw()
    if script_draw:
      script.draw()
    pygame.display.update()


# Cannot be put in a try/catch because errors will disappear while still killing the program.
loop = asyncio.get_event_loop()
loop.run_until_complete(main())