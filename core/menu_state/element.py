
class element:
  def __init__(this, x, y, w, h, style):
    this.x = x
    this.y = y
    this.w = w
    this.h = h
    this.style = style
    this.children = []
  
  def __del_prop(this):
    pass # Dummy because deleting these makes no sense
  def __get_r(this):
    return this.x+this.w
  def __set_r(this, val):
    this.w = val-this.x
  def __get_d(this):
    return this.y+this.h
  def __set_d(this, val):
    this.h = val-this.y
  d = property(fget=__get_d, fset=__set_d, fdel=__del_prop, doc="down/bottom: changes dimensions, not position")
  r = property(fget=__get_r, fset=__set_r, fdel=__del_prop, doc="right:changes dimensions, not position")
  
  def to_element_coords(this, x, y):
    return ((x-this.x)/this.w, (y-this.y)/this.h)

  def to_exterior_coords(this, x, y):
    return ((x*this.w)+this.x, (y*this.h)+this.y)
  
  def draw_self(this, stx, sty, stw, sth):
    pass

  def draw_children(this, stx, sty, stw, sth):
    for child in this.children:
      child.draw(stx, sty, stw, sth)

  def draw(this, stx, sty, stw, sth):
    pass

  def intersect(this, x, y, w, h):
    pass

  class style:
    def __init__(this):
      this.fill = (0,0,0,0)
      this.outline_color = (0, 0, 0, 0)
      this.outline_width = 0
      this.text = ""
    
    def hasOutline(this):
      return this.outline_width > 0 and this.outline_color[3] > 0
