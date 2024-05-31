import math
import entity
import pygame
from core.globals import screen

# Singleton class for the player, allowing it to inherit properly from entity.
# Constructing new instances is ill-advised, though technically possible.
class player_class(entity):
  # Set of all valid player variants.
  # Key: id, Val: filename
  variants = {
    "base": "base"
  }

  def __init__(this):
    # Player is created at the bottom center of the screen facing upwards by default.
    entity.__init__(this, "player", screen.w/2, screen.h - 128, -90, 128/512)
    this.health = 100
    this.radius = 64
    this.setVariant()
  
  def setVariant(this, var = "base"):
    # Optionally set variant of this player
    this.variant = var

    # Reset invalid variants
    if not (this.variant in player_class.variants):
      this.variant = player_class.variants["base"]
    
    # General loading
    this.sprite = pygame.image.load(f"assets\image\player\player_{this.variant}.png")
    this.update_graphics()

  # Called after game is loaded and player entity is created.
  def load(this, var = "base"):
    this.setVariant(var)

  def damage(this, amt):
    this.health -= amt # Limited effects for now

  def update(this, dt):
    entity.update(this, dt)

