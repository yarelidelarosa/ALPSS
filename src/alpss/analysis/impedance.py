import math
class Material: 
  def __init__(self, density, C0, S, name=""):#p(density), bulk sound speed(C0), Hugonoit slope(S)
    if density<=0:
      raise ValueError("density must be a positive number")
    if C0<= 0:
      raise ValueError("C0 must be a positive number")
    self.density=density
    self.C0=C0
    self.S=S
    self.name=name
def is_symmetric_impact (flyer,target):
  if target is None: 
    return True
  tiny=0.000001  #2 numbers are the same if they have small difference 
  same_density=abs(flyer.density-target.density) < tiny
  same_C0=abs(flyer.C0 - target.C0) < tiny
  same_S =abs(flyer.S - target.S) < tiny
  
  return same_density and same_C0 and same_S

def check_case1 (flyer, target):
  if target is None: 
    return False
  flyer_impedance=flyer.density*flyer.C0
  target_impedance = target.density*target.C0
  return target_impedance > flyer_impedance
  
def particle_velocity(flyer_velocity, flyer, target=None): 
  V=flyer_velocity
  if V < 0: 
    raise ValueError ("flyer_velocity must be 0 or positive")
  if check_case1(flyer, target):  #same material on both sides
    return V/2
  #Different materials-->solve a*u_p^2 + b*u_p + c = 0
  a=target.density*target.S - flyer.density*flyer.S
  b=(target.density*target.C0+2*flyer.density*flyer.S*V)
  C=-flyer.density*V*(flyer.C0+flyer.S*V)
  if abs(a) < 1e-12:  #if a is around 0 the u_p^2 term disappears
    return -c/b
  #otherwise-->quadratic formula to solve
  discriminant=b*b-4*a*c
  root1=(-b+math.sqrt(discriminant))/(2*a)
  root2=(-b-math.sqrt(discriminant))/(2*a)

  if 0<=root1<=V:    #particle velocity has to be between 0 and impact speed V. Returns speed that makes sense
    return root1
  else: 
    return root2
