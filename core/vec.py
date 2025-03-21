import math

class vec:
  def __init__(this, x, y=None):
    if isinstance(x, vec):
      this.x = x.x
      this.y = x.y
    else:
      this.x = x
      if y==None:
        this.y = x
      else:
        this.y = y

  def __get_l(this):
    return math.sqrt(this.x*this.x + this.y*this.y)
  
  def __set_l(this, val):
    current_l = math.sqrt(this.x*this.x + this.y*this.y)
    this.x *= val/current_l
    this.y *= val/current_l

  def __del_l(this):
    pass

  l = property(
    fget = __get_l,
    fset = __set_l,
    fdel = __del_l,
    doc = "Length (property)"
  )

  def __get_a(this):
    return math.atan2(this.y, this.x)
  
  def __set_a(this, val):
    current_l = this.l
    this.x = current_l * math.cos(val)
    this.y = current_l * math.sin(val)
  
  def __del_a(this):
    pass

  a = property(
    fget = __get_a,
    fset = __set_a,
    fdel = __del_a,
    doc = "Angle (property)"
  )

  # Returns a copy of this vector normalized to a length of 1
  def norm(this):
    current_l = this.l
    return vec(this.x/current_l, this.y/current_l)

  def dot(this, other):
    return this.x*other.x + this.y*other.y

  # Returns the acute angle between this vector and another
  def angle(this, other):
    # Credit: https://stackoverflow.com/a/35134034
    determinant = this.cross(other)
    dotproduct = this.dot(other)
    return math.atan2(determinant, dotproduct)
  
  # Note: this is the 2d cross product. 3d cross product is not considered.
  # Also known as the determinant.
  def cross(this, other):
    return this.x*other.y - this.y*other.x

  def __add__(this, other):
    return vec(this.x + other.x, this.y + other.y)
  
  def __sub__(this, other):
    return vec(this.x - other.x, this.y - other.y)
  
  def __mul__(this, other):
    if isinstance(other, vec):
      return vec(this.x * other.x, this.y * other.y)
    else:
      return vec(this.x * other, this.y * other)
    
  def __truediv__(this, other):
    if isinstance(other, vec):
      return vec(this.x / other.x, this.y / other.y)
    else:
      return vec(this.x / other, this.y / other)
    
  def __mod__(this, other):
    if isinstance(other, vec):
      return vec(this.x % other.x, this.y % other.y)
    else:
      return vec(this.x % other, this.y % other)
  
  def __pow__(this, other):
    if isinstance(other, vec):
      return vec(pow(this.x, other.x), pow(this.y, other.y))
    else:
      return vec(pow(this.x, other), pow(this.y, other))
  
  def __eq__(this, other):
    if isinstance(other, vec):
      return this.x == other.x and this.y == other.y
    return False
  
  def __neg__(this):
    return vec(-this.x, -this.y)
  
  def __pos__(this):
    return vec(+this.x, +this.y)
  
  def __invert__(this):
    return vec(this.y, this.x)
  
  def __str__(this):
    return "("+str(this.x)+","+str(this.y)+")"