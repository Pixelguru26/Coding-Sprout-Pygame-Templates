from core.module_entity.entity import entity
from core.graphics.img import image
from core import player
from core.globals import entities, bullets, entityque

class sprite(entity):
  type = "sprite"

  def __init__(this, imgpath):
    entity.__init__(this)
    this.sprite = image(imgpath)
    entityque.append(this)
  
def __collides_with_any(this, type = "any"):
  if type == "enemy":
    for ent in entities:
      if ent.team == "enemy":
        if this.intersects(ent):
          return True
  elif type == "player":
    return this.intersects(player)
  elif type == "entity":
    for ent in entities:
      if this.intersects(ent):
        return True
  elif type == "bullet":
    for ent in bullets:
      if this.intersects(ent):
        return True
  elif type == "sprite":
    for ent in entities:
      if ent.type == "sprite":
        if this.intersects(ent):
          return True
  else:
    for ent in entities:
      if this.intersects(ent):
        return True
    for ent in bullets:
      if this.intersects(ent):
        return True
    return this.intersects(player)
  return False
entity.collides_with_any = __collides_with_any

def __collisions(this, type = "any"):
  ret = []
  if type == "enemy":
    for ent in entities:
      if ent.team == "enemy" and this.intersects(ent):
        ret.append(ent)
  elif type == "player":
    if this.intersects(player):
      ret.append(player)
  elif type == "entity":
    for ent in entities:
      if this.intersects(ent):
        ret.append(ent)
  elif type == "bullet":
    for ent in bullets:
      if this.intersects(ent):
        ret.append(ent)
  elif type == "sprite":
    for ent in entities:
      if ent.type == "sprite" and this.intersects(ent):
        ret.append(ent)
  else:
    for ent in entities:
      if this.intersects(ent):
        ret.append(ent)
    for ent in bullets:
      if this.intersects(ent):
        ret.append(ent)
    if this.intersects(player):
      ret.append(player)
  return ret
entity.collisions = __collisions