import math
class Material: #stores 3 shock numbers a material needs: 
  def __init__(self, density, C0, S, name=""):#p(density), bulk sound speed(C0), Hugonoit slope(S)
    #rfuse impossible values
    if density<=0:
      raise ValueError("density must be a positive number")
    if C0<= 0:
      raise ValueError("C0 must be a positive number")
    self.density=density
    self.C0=C0
    self.S=S
    self.name=name 
def is_symmetric_impact (flyer,target):
  #return TRUE if lfyer and sample are same material
  # answer is V/2 in that case

  if target is None: #target=None means "no smaple given", treat same as  same-as-flyer
    return True
  tiny=0.000001  #2 numbers are the same if they have small difference 
  same_density=abs(flyer.density-target.density) < tiny
  same_C0=abs(flyer.C0 - target.C0) < tiny
  same_S =abs(flyer.S - target.S) < tiny
  
  return same_density and same_C0 and same_S#only symmetric if all 3 properties match

def check_case1 (flyer, target):
  #Return True for the textbook's "Case 1": a shock going into a
  #HIGHER-impedance target (page 46). Impedance here is the acoustic
  #impedance Z = density * C0 (the impedance in the weak-shock limit).
  #  target stiffer than flyer  -> Case 1  -> True
  #  target softer  than flyer  -> Case 2  -> False
  if target is None: 
    #same material or no target -> no mismatch, so neither case
    return False
  flyer_impedance = flyer.density*flyer.C0
  target_impedance = target.density*target.C0
  return target_impedance > flyer_impedance
  
def particle_velocity(flyer_velocity, flyer, target=None): 
  #returns the particle velocity at the flyer/sample interface in m/s.
  #  flyer_velocity : impact speed V, m/s (a single number, must be >= 0)
  #  flyer          : a Material (the book's Material I)
  #  target         : a Material (the book's Material II). Leave it out (None) to mean "same material as the flyer".
  V=flyer_velocity
  if V < 0: #impact speed can't be negative
    raise ValueError ("flyer_velocity must be 0 or positive")
  if is_symmetric_impact(flyer, target):  #same material on both sides
    return V/2
  


  #Different materials-->solve a*u_p^2 + b*u_p + c = 0
  #These three lines ARE Equation 3.11, rearranged into a normal quadratic.
  #They come from setting the flyer's pressure equal to the sample's pressure
  #at the interface (with u_g = V/2) and collecting the u_p terms. In the
  a=target.density*target.S - flyer.density*flyer.S
  b=(target.density*target.C0+flyer.density*flyer.C0+2*flyer.density*flyer.S*V)
  c=-flyer.density*V*(flyer.C0+flyer.S*V)
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
