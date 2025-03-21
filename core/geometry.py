import math
import core.util as util
from core.vec import vec

# Geometric calculations
# ==========================================
# Returns the y value of the provided line at the x coordinate xtest
# Does not check boundaries
# If the line is vertical, returns nan
def line_y(xtest, x1, y1, x2, y2):
  if (x1 == x2):
    return math.nan
  if (y1 == y2):
    return y1
  # Reinterpolation. Perhaps not the most efficient, but it makes sense.
  return (xtest-x1) / (x2-x1) * (y2-y1) + y1

# Returns the x value of the provided line at the y coordinate ytest
# Does not check boundaries
# If the line is horizontal, returns nan
def line_x(ytest, x1, y1, x2, y2):
  if (y1 == y2):
    return math.nan
  if (x1 == x2):
    return x1
  # Reinterpolation. Perhaps not the most efficient, but it makes sense.
  return (ytest-y1) / (y2-y1) * (x2-x1) + x1

# Returns a tuple of (x, y) representing the point v interpolated along the line
def line_lerp(v, x1, y1, x2, y2):
  return (v*(x2-x1)+x1, v*(y2-y1)+y1)

# Simply returns the slope of the provided line.
# If the line is vertical, returns nan.
def line_slope(x1, y1, x2, y2):
  if (x1 == x2):
    return math.nan
  return (y2-y1)/(x2-x1)

# This technically just returns the normalized dot product of the point (vx,vy) onto the line
# To get the actual projection, you would use result*(p2-p1)+p1
# where p1 = (x1,y1) and p2 = (x2,y2)
def line_delerp(vx, vy, x1, y1, x2, y2):
  bx = x2 - x1
  by = y2 - y1
  return ((vx-x1)*bx + (vy-y1)*by) / (bx*bx + by*by)

# Returns the so-called "2-dimensional cross product" of (x1,y1) and (x2,y2)
# This can be thought of as the area of a parallelogram formed from these vectors.
# Unlike area, however, this result is signed.
# When (x2,y2) is on the "right" side of (x1,y1), the area is positive.
# When (x2,y2) is on the "left" side of (x1,y1), the area is negative.
# When (x2,y2) lies along (x1,y1), the area is 0.
def cross(x1, y1, x2, y2):
  return x1*y2-y1*x2

# Rotates the point (x,y) 90 degrees clockwise about the origin (ox,oy)
def rotate_point_90(ox, oy, x, y):
  return (ox-(y-oy), oy+(x-ox))

# Rotates the point (x,y) about the origin (ox,oy) using precalculated sin and cos values.
def rotate_point(ox, oy, x, y, sin, cos):
  return ((x-ox) * cos - (y-oy) * sin + ox, (x-ox) * sin + (y-oy) * cos + oy)

# Checks if a point is within the bounds of the provided parallelogram.
# The parallelogram must have one point on the origin,
# and be defined by two vectors corresponding to A->B and A->D
def point_in_originated_parallelogram(px, py, ax, ay, bx, by):
  # Orthogonal vectors a' and b'
  apx = -ay
  apy = ax
  bpx = -by
  bpy = bx
  # Oriented vectors a'' and b'' ((a) (d)ouble (p)rime)
  adpsign = util.sign(util.dot(apx, apy, bx, by))
  adpx = adpsign * apx
  adpy = adpsign * apy
  bdpsign = util.sign(util.dot(ax, ay, bpx, bpy))
  bdpx = bdpsign * bpx
  bdpy = bdpsign * bpy
  # Boundary check
  check = util.dot(adpx, adpy, px, py)
  bound = util.dot(adpx, adpy, bx, by)
  if not (0 <= check and check <= bound): return False
  check = util.dot(bdpx, bdpy, px, py)
  bound = util.dot(ax, bx, bdpx, bdpy)
  return 0 <= check and check <= bound

# Checks if a point is within the bounds of a provided parallelogram.
# px, py: coordinates of the point to check
# ax, ay, etc: coordinates of the four points of the parallelogram, in clockwise order
def point_in_parallelogram(px, py, ax, ay, bx, by, cx, cy, dx, dy):
  return point_in_originated_parallelogram(px - ax, py - ay, bx - ax, by - ay, dx - ax, dy - ay)

# ==========================================
# Line intersection
# ==========================================
# tldr: use "lineseg_intersection" to find the point of intersection between two line segments.
# That's all this entire section does.
# If you just need to know *if* a pair intersects, use intersect_line

# Rotates a line 90 degrees clockwise about the origin (ox,oy)
# This direction is considered the "clockwise" or "positive" normal
def rotate_line_90(ox, oy, x1, y1, x2, y2):
  (rx1, ry1) = rotate_point_90(ox, oy, x1, y1)
  (rx2, ry2) = rotate_point_90(ox, oy, x2, y2)
  return (rx1, ry1, rx2, ry2)

# Returns the clockwise normal vector of the line multiplied by its length
# If length is inconsequential, this is preferred
def line_normal_quick(x1, y1, x2, y2):
  return (y1-y2, x2-x1)

# Returns the clockwise normal vector of the line
# Relatively high performance cost
def line_normal(x1, y1, x2, y2):
  return util.normalize(y1-y2, x2-x1)

# Returns (t, u) where each are the interpolation factors of intersection
# for the lines a and b, respectively.
# In non-intersecting cases, returns (nan, nan) or (inf, inf)
# (nan, nan) corresponds to collinear lines which may or may not intersect.
# (inf, inf) corresponds to parallel, non-intersecting lines.
def line_intersection_tu(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
  # Credit: https://stackoverflow.com/a/565282
  # I gave up on trying to keep track of things without vectors
  a1 = vec(ax1, ay1)
  a2 = vec(ax2, ay2)
  b1 = vec(bx1, by1)
  b2 = vec(bx2, by2)
  da = a2-a1 # "delta a," dimensions of a
  db = b2-b1 # "delta b," dimensions of b
  # A bit of math because I'm dumb
  #            a1 + t*da = b1 + u*db
  #     (a1 + t*da) x db = (b1 + u*db) x db
  #                      = b1 x db + u(db x db)
  # a1 x db + t(da x db) = b1 x db
  #           t(da x db) = (b1 x db) - (a1 x db)
  #           t(da x db) = (b1 - a1) x db
  #                    t = [(b1 - a1) x db] / [da x db]
  do = b1 - a1
  rxs = da.cross(db)
  if rxs == 0:
    if do.cross(da) == 0:
      # Collinear, may or may not intersect
      return (math.nan, math.nan)
    else:
      # Parallel, non-intersecting
      return (math.inf, math.inf)
  else:
    # Lines intersect, segments still may not
    return (
      do.cross(db) / rxs,
      do.cross(da) / rxs
    )

# Returns (x, y) indicating the point where the lines intersect.
# If the lines do not intersect, returns (nan, nan).
def line_intersection_point(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
  (t, u) = line_intersection_tu(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2)
  if math.isfinite(t):
    return line_lerp(t, ax1, ay1, ax2, ay2)
  else:
    return (math.nan, math.nan)

# Returns (a, x, y) where a is a boolean indicating whether the lines intersect at all
def lineseg_intersection_point(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
  (t, u) = line_intersection_tu(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2)
  if not math.isfinite(t):
    return (False, t, u)
  if t < 0 or t > 1 or u < 0 or u > 1:
    return (False, math.nan, math.nan)
  (x, y) = line_lerp(t, ax1, ay1, ax2, ay2)
  return (True, x, y)

# Returns the nearest point to (x,y) on line a
def line_nearest_point(x, y, ax1, ay1, ax2, ay2):
  (px, py) = util.project(x-ax1, y-ay1, ax2-ax1, ay2-ay1)
  return (px + ax1, py + ay1)

# ==========================================
# Point inclusion checks
# ==========================================
def point_in_aabb(x, y, ax, ay, aw, ah):
  return (x >= ax) and (x <= ax+aw) and (y >= ay) and (y <= ay+ah)

def point_in_circle(x, y, ax, ay, ar):
  return util.dist(x, y, ax, ay) <= ar

# Returns True if the point (x,y) is within range of line a
def point_on_line(x, y, range, ax1, ay1, ax2, ay2):
  (px, py) = line_nearest_point(x, y, ax1, ay1, ax2, ay2)
  return util.dist(px, py, x, y) <= range

# Returns True if the point is on the "left" side of the line
# This is determined by line point order
def point_behind_line(x, y, ax1, ay1, ax2, ay2):
  return cross(ax2-ax1, ay2-ay1, x-ax1, y-ay1) <= 0

# ==========================================
# AABB broadphase checks
# ==========================================
def broadphase_aabb_aabb(ax, ay, aw, ah, bx, by, bw, bh):
  return bx <= ax+aw and bx+bw >= ax and by <= ay+ah and by+bh >= ay

def broadphase_circle_circle(ax, ay, ar, bx, by, br):
  return broadphase_aabb_aabb(ax-ar, ay-ar, ar*2, ar*2, bx-br, by-br, br*2, br*2)

def broadphase_line_line(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
  return broadphase_aabb_aabb(ax1, ay1, ax2-ax1, ay2-ay1, bx1, by1, bx2-bx1, by2-by1)

def broadphase_aabb_circle(ax, ay, aw, ah, bx, by, br):
  return broadphase_aabb_aabb(ax, ay, aw, ah, bx - br, by - br, br*2, br*2)

def broadphase_aabb_line(ax, ay, aw, ah, bx1, by1, bx2, by2):
  return broadphase_aabb_aabb(ax, ay, aw, ah, bx1, by1, bx2-bx1, by2-by1)

def broadphase_circle_line(ax, ay, ar, bx1, by1, bx2, by2):
  return broadphase_aabb_aabb(ax-ar, ay-ar, ar*2, ar*2, min(bx1, bx2), min(by1, by2), abs(bx2-bx1), abs(by2-by1))

# ==========================================
# Intersection tests (boolean)
# ==========================================
intersect_aabb = broadphase_aabb_aabb

def intersect_circle_raw(ax, ay, ar, bx, by, br):
  return (math.sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay)) <= ar + br)

def intersect_circle(ax, ay, ar, bx, by, br):
  return broadphase_circle_circle(ax, ay, ar, bx, by, br) and (math.sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay)) <= ar + br)

def intersect_aabb_circle(x1, y1, w, h, circlex, circley, radius):
  if not broadphase_aabb_circle(x1, y1, w, h, circlex, circley, radius):
    return False
  if point_in_aabb(circlex, circley, x1, y1-radius, w, h+radius*2):
    return True
  if point_in_aabb(circlex, circley, x1-radius, y1, w+radius*2, h):
    return True
  if circlex < x1+w/2: # Left side
    if circley < y1+h/2: # Top left
      return point_in_circle(x1, y1, circlex, circley, radius)
    else: # Bottom left
      return point_in_circle(x1, y1+h, circlex, circley, radius)
  else: # Right side
    if circley < y1+h/2: # Top right
      return point_in_circle(x1+w, y1, circlex, circley, radius)
    else: # Bottom right
      return point_in_circle(x1+w, y1+h, circlex, circley, radius)

def intersect_line(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
  if not broadphase_line_line(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    return False
  (t, u) = line_intersection_tu(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2)
  return math.isfinite(t) and t >= 0 and t <= 1 and u >= 0 and u <= 1

def intersect_aabb_line(boxx, boxy, boxw, boxh, linex1, liney1, linex2, liney2):
  if not broadphase_aabb_line(boxx, boxy, boxw, boxh, linex1, liney1, linex2, liney2):
    return False
  if point_in_aabb(linex1, liney1, boxx, boxy, boxw, boxh) or point_in_aabb(linex2, liney2, boxx, boxy, boxw, boxh):
    return True
  # Tests box edges in clockwise order from the top left corner
  return (
    intersect_line(linex1, liney1, linex2, liney2, boxx, boxy, boxx+boxw, boxy) or
    intersect_line(linex1, liney1, linex2, liney2, boxx+boxw, boxy, boxx+boxw, boxy+boxh) or
    intersect_line(linex1, liney1, linex2, liney2, boxx+boxw, boxy+boxh, boxx, boxy+boxh) or
    intersect_line(linex1, liney1, linex2, liney2, boxx, boxy+boxh, boxx, boxy)
  )

# Methodology:
#   Check broad phase (aabb) collisions as shortcut to false
#   Check if the circle center is outside the length of the line segment:
#     Check if the circle intersects with one of the line endpoints
#   else:
#     Check if the nearest point on the line intersects with the circle
def intersect_circle_line(circlex, circley, radius, linex1, liney1, linex2, liney2):
  if not broadphase_circle_line(circlex, circley, radius, linex1, liney1, linex2, liney2):
    return False
  dotprod = line_delerp(circlex, circley, linex1, liney1, linex2, liney2)
  if dotprod < 0 or dotprod > 1:
    return (
      math.sqrt((circlex-linex1)*(circlex-linex1)+(circley-liney1)*(circley-liney1)) <= radius or
      math.sqrt((circlex-linex2)*(circlex-linex2)+(circley-liney2)*(circley-liney2)) <= radius
    )
  else:
    projx = dotprod*(linex2-linex1)+linex1
    projy = dotprod*(liney2-liney1)+liney1
    return math.sqrt((circlex-projx)*(circlex-projx) + (circley-projy)*(circley-projy)) <= radius
