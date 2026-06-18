from alpss.analysis.impedance import Material, particle_veloctiy, check_case1

#(density, C0 (speed of sound), S (), name)
#(kg/m^3, m/s, number)
COPPER= Material (8960.0, , "Copper") #from MIT website, thier material prop. database
#calc. for speed of sound in documentation
ALUMINUM= Material (2700.0, , "Aluminum") #from MIT website, thier material prop. database
#calc. for speed of sound in documentation

def close (a,b):
  return abs(a - b) < 1e-6*max(1.0,abs(a),abs(b))
def pressure_sample (material, u):
  return material.density* (material.C0 + material.S* u) * u
def pressure_flyer (material, u, V):
  return material.density * (material.C0 + material.S * (V-u)) * (V-u)

if __name__=="__main__": 
  print ("")
