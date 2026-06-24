from alpss.analysis.materials import (get_material, list_materials, material_from_config, materials_from_config)
from alpss.analysis.impedance import Material, particle_velocity

def close (a,b):
    return abs(a - b) < 1e-6*max (1.0, abs(a), abs(b))

def test_get_material_values():
    cu=get_material("copper")
    assert close (cu.density, 8960.0)
    assert close (cu.C0, 3958.37)
    assert close (cu.S, 1.489)

def test_get_material_not_case_sensitive():
    for name in ["copper", "Copper", "COPPER", "  copper  "]:
        m = get_material (name)
        asssert close (m.density, 8960)

def test_unknown_material_is_rejected():
    try:
        get_material("vibranium")
        assert False, "expected a Value error for an unknown material"
    except ValueError:
        pass

def test_list_materials():
    names = list_materials ()
    assert "copper" in names
    assert "glass" in names
    assert len (names) == 4
