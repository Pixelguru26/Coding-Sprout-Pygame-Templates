
class cacheimg:
  def __init__(this, id, srcimg):
    this.cache = {
      0: {
        1: srcimg
      }
    }
    this.cache[1] = {}
    this.cache[1][0] = srcimg
  
  def index(this, angle, scale):
    pass
