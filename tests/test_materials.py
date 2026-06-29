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
        assert close (m.density, 8960)

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

def test_material_from_config_by_numbers():
    cfg={"density": 2700.0, "C0": 4830.46, "S": 1.338}
    m = material_from_config(cfg)
    assert close (m.density, 2700.0) and close (m.C0, 4830.46) and close(m.S, 1.338)

def test_material_from_config_flyer_prefix():
    cfg={"flyer_material": "titanium"}
    m = material_from_config(cfg, "flyer_")
    assert close (m.density, 4510.0)

def test_no_flyer_means_same_as_sample():
    cfg ={"material":"copper"}
    flyer, target = materials_from_config(cfg)
    assert close (flyer.density, target.density)
    assert close (flyer.C0, target.C0)
    assert close (flyer.S, target.S)

def test_flyer_and_target_differ():
    cfg={"material":"glass", "flyer_material":"copper"}
    flyer, target = materials_from_config (cfg)
    assert close (flyer.density, 8960.0) #copper
    assert close (target.density, 2440.0) #glass

def test_database_materials_works_with_particle_velocity():
    cu = get_material("copper")
    glass = get_material("glass")
    assert close (particle_velocity(1000.0, cu), 500.0)#copper into glass->faster than half
    u_p = particle_velocity (1000.0, cu, glass)
    assert u_p > 500.0
    #looking up materials sould match to done by hand
    cu_byhand = Material(8960.0, 3958.37, 1.489)
    glass_byhand = Material(2440, 4198, 1.61)
    assert close (u_p, particle_velocity(1000.0, cu_byhand, glass_byhand))

if__name__=="__main__": 