from alpss.analysis.impedance import Material, particle_veloctiy, check_case1

COPPER
ALUMINUM

def close (a,b):
  return abs(a - b) < 1e-6*max(1.0,abs(a),abs(b))
def pressure_sample (material, u):
  return material.density* (material.C0 + material.S* u) * u
def pressure_flyer (material, u, V):
  return material.density * (material.C0 + material.S * (V-u)) * (V-u)
  
