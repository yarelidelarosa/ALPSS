from alpss.analysis.impedance import Material
MATERIAL_TABLE = {
  "copper": (8960.0, 3958.37, 1.489), 
  "aluminum": (2700.0, 4830.46, 1.338), 
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
  return Material(density, C0, S, name=name)

def material_from_confrig(inputs, prefix=""):
  name_key=prefix+"material"

  if inputs.get(name_key):
    return get_material(inputs[name_key])

  density = inputs[prefix+"density"]
  C0=inputs[prefix+"C0"]
  S = inputs.get(prefix + "S", 0.0)
  return Material (density, C0, S, name=inputs.get(name_key, ""))

def materials_from_confrig(inputs): 
  target = material_from_confrig(inputs, prefix="")
  flyer_given= False
  if"flyer_material" in inputs and inputs ["flyer_material"] !="":
    flyer_given =True
  if "flyer_density" in inputs: 
    flyer_given = True

  if flyer_given: 
    flyer = material_from_confrig(inputs, prefix="flyer")
  else: 
    flyer = target
  return flyer, target
  
