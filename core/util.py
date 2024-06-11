import math


# Simple clamp function.
# Returns v restricted to the range [a, b] (inclusive)
def clamp(v, a, b):
  if v < a: return a
  if v > b: return b
  return v

# Simple wrap function.
# Returns v restricted to the range [a, b), wrapping when necessary
def wrap(v, a, b):
  return (v - a)%(b - a) + a

# Simple linear interpolation on one axis.
# Returns the number a fraction (v) of the way between a and b.
# Does not perform clamping before operation.
def lerp(v, a, b):
  return v*(b-a)+a

# Vector projection of (x, y) onto a line segment defined by two other vectors (x1, y1 and x2, y2).
# Takes six arguments, corresponding to three vectors: (x, y), (x1, y1), and (x2, y2).
# Equivalent to traditional vector projection when x1, y1 = 0, 0
# Returns x, y of the resulting vector
def project(x, y, x1, y1, x2, y2):
  rx = x - x1
  ry = y - y1
  dx = x2 - x1
  dy = y2 - y1
  dotprod = (rx * dx + ry * dy)
  factor = dotprod / (dx * dx + dy * dy)
  return x1 + factor * dx, y1 + factor * dy

# Distance between two points, represented as four arguments
def dist(x1, y1, x2, y2):
  dx = x2 - x1
  dy = y2 - y1
  return math.sqrt(dx * dx + dy * dy)

# Simplest possible sign function with no failure case.
# sign(-inf) returns -1
# sign(inf) returns 1
# default return for non-numbers and NaN is 0
def sign(v):
  if isinstance(v, (int, float, complex)) and not isinstance(v, bool):
    if math.isnan(v):
      return 0
    if v < 0:
      return -1
    if v > 0:
      return 1
  return 0
