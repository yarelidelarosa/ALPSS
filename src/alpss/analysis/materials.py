from alpss.analysis.impedance import Material
MATERIAL_TABLE = {
  "copper": (8960.0, 3958.37, 1.489), 
  "aluminum": (2700.0, 4830.46, 1.338), 
  "glass": (2440, 4198, 1.61),
  "titanium": (4510.0, 4961.0,  0.957),
}
def list_materials():
  return sorted(MATERIAL_TABLE.keys())

def get_material(name):
  key=name.strip().lower()
  if key not in MATERIAL_TABLE:
    raise ValueError(
      "Unknown material'"+str(name)+"'."
      "Known materials are:"+", ".join(list_materials())
    )
  density, C0, S = MATERIAL_TABLE[key]
  return Material(density, C0, S, name)

def material_from_config(inputs, prefix=""):
  name_key=prefix+"material"

  if name_key in inputs and inputs[name_key]:
    return get_material(inputs[name_key])

  density = inputs[prefix+"density"]
  C0=inputs[prefix+"C0"]
  if  (prefix + "S") in inputs:
    S = inputs[prefix + "S"]
  else: 
    S = 0.0 #if S is missing, assume 0
  return Material (density, C0, S)

def materials_from_config(inputs): 
  target = material_from_config(inputs, "")
  flyer_given= False
  if"flyer_material" in inputs and inputs ["flyer_material"] !="":
    flyer_given =True
  if "flyer_density" in inputs: 
    flyer_given = True

  if flyer_given: 
    flyer = material_from_config(inputs, prefix="flyer_")
  else: 
    flyer = target
  return flyer, target
  
