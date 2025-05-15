import tempfile
import os
from .utils import update_yaml
import re
import subprocess

def simulate(variables: dict):
    temp_dir = tempfile.gettempdir()
    fits_file_path = os.path.join(temp_dir, "simulation_result.fits")
    mode, source, exp = variables["mode"], variables["source"], variables["exposure_time"] 
    lss_pattern = re.compile("lss_[lnm]")

    yaml_lss_updates = {
    ("lss_l", "simple_gal"): {"do.catg": "LM_LSS_SCI_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "L_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,LM", "properties:type": "OBJECT"},
    ("lss_l", "empty_sky"): {"do.catg": "LM_LSS_SKY_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "L_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,LM", "properties:type": "SKY"},
    ("lss_l", "simple_star8"): {"do.catg": "LM_LSS_STD_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "L_spec", "properties:catg": "CALIB", "properties:tech": "LSS,LM", "properties:type": "STD"},
    ("lss_n", "simple_gal"): {"do.catg": "N_LSS_SCI_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,N", "properties:type": "OBJECT"},
    ("lss_n", "empty_sky"): {"do.catg": "N_LSS_SKY_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,N", "properties:type": "SKY"},
    ("lss_n", "simple_star8"): {"do.catg": "N_LSS_STD_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N_spec", "properties:catg": "CALIB", "properties:tech": "LSS,N", "properties:type": "STD"},
    }

    if lss_pattern.match(mode):
        key = (mode, source)
        if key in yaml_lss_updates:
            yaml_changes = {f"simulation:{k}": v for k, v in yaml_lss_updates[key].items()}
            update_yaml("sim.yaml", yaml_changes)
        else:
            raise ValueError(f"Unsupported mode/source combination: {key}")
    else:
        raise ValueError("Unsupported mode(How did you even select that?)")
    cmd = [
        "python/run_recipes.py",
        "--inputYAML=sim.yaml",
        "--outputDir", f"{temp_dir}",
        "--doCalib=0",
        "--sequence=1",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)