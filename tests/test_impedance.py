from alpss.analysis.impedance import Material, particle_veloctiy, check_case1

#(density, C0 (speed of sound), S (), name)
#(kg/m^3, m/s, number)
COPPER= Material (8960.0, 3958.37, 1.489, "Copper") #from MIT website, thier material prop. database
#calc. for speed of sound in 
GLASS = Material(2440, 4198, 1.61, "Glass")
ALUMINUM= Material (2700.0, 4830.46, 1.338,"Aluminum") #from MIT website, thier material prop. database
#calc. for speed of sound in documentation
TITANIUM = Material (4510.0, 4961.0, 0.957, "Titanium")

def close (a,b):
  return abs(a - b) < 1e-6*max(1.0,abs(a),abs(b))
def pressure_sample (material, u):
  return material.density* (material.C0 + material.S* u) * u
def pressure_flyer (material, u, V):
  return material.density * (material.C0 + material.S * (V-u)) * (V-u)
def test_same_material_gives_half():
  for V in [10.0, 100.0, 1000.0, 3000.0]:
    assert close (particle_velocity(V, COPPER), V/2)
    assert close (particle_velocity(V,COPPER, COPPER), V/2)

def test_pressures_match_for_different_materials():
  pairs= [(COPPER, GLASS), (GLASS, COPPER), (TITANIUM, ALUMINUM), (ALUMINUM, TITANIUM)]
  for flyer, sample in pairs: 
    V=1500.0
    u_p=particle_velocity(V, flyer, sample)
    assert close (pressure_flyer(flyer, u_p,V), pressure_sample(sample, u_p))

def test_answer_is_between_zero_and_V():
  V=1500.0
  for flyer, sample in [(COPPER, GLASS), (GLASS, COPPER), (ALUMINUM, TITANIUM)]: 
    u_p=particle_velocity (V, flyer, sample)
    assert 0.0 < u_p < V

def test_stiff_vs_soft_direction():
  assert particle_velocity(1000.0, COPPER, GLASS) > 500.0
  assert particle_velocity(1000.0, GLASS, COPPER) < 500.0

def test_check_case1():
  assert check_case1 (COPPER, None) is True #no sample given
  assert check_case1 (COPPER, COPPER) is True #same material
  assert check_case1 (COPPER, GLASS) is False #different materials

def test_zero_speed_gives_zero():
  assert particle_velocity(0.0, COPPER, GLASS) == 0.0

def test_negative_speed_is_rejected():
  try:
    particle_velocity(-1.0, COPPER)
    assert False, "expeced ValueError for negative speed"
  except ValueError: 
    pass #raised error

def test_bad_material_is_rejected():
  try:
    Material(-100.0, 3958.37, 1.489)
    assert False, "expected a ValueError for negative density"
  except ValueError: 
    pass
  
if __name__=="__main__": 
  test_same_material_gives_half()
  test_pressures_match_for_different_materials()
  test_answer_is_between_zero_and_V()
  test_stiff_vs_soft_direction()
  test_check_case1()
  test_zero_speed_gives_zero()
  test_negative_speed_is_rejected()
  test_bad_material_is_rejected()
  print ("tests passed")
