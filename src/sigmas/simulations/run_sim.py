import tempfile
import os
from .utils import update_yaml, yaml_lss_updates, get_scopesim_inst_pkgs_path, ensure_packages_installed
import re
import subprocess
import sys
import scopesim as sim
from pathlib import Path

def Simulate(variables: dict):

    packages_path = get_scopesim_inst_pkgs_path()
    print(f"Using packages path: {packages_path}")
    
    # Convert packages_path to Path object for consistent handling
    packages_path = Path(packages_path)
    
    # Set the local packages path before anything else
    sim.rc.__config__["!SIM.file.local_packages_path"] = str(packages_path)
    
    try:
        ensure_packages_installed()
        
        # Instead of adding the base path, add each required package path
        required_packages = ["METIS", "ELT", "Armazones"]
        sim.rc.__config__["!SIM.file.local_packages_path"] = str(packages_path)
        sim.commands.user_commands.add_packages_to_rc_search(
            local_path=str(packages_path),
            package_list=required_packages
        )
                
    except Exception as e:
        print(f"Failed to initialize packages: {str(e)}")
        raise


    temp_dir = tempfile.gettempdir()
    fits_file_path = os.path.join(temp_dir, "simulation_result")
    mode, source, exp = variables["mode"], variables["source"], variables["exposure_time"] 
    lss_pattern = re.compile("lss_[lnm]")
    this_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(this_dir, "sim.yaml")

    # Add debug output for YAML path resolution
    print("\nDebug: YAML File Location")
    print("-" * 50)
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory (this_dir): {this_dir}")
    print(f"YAML path: {yaml_path}")
    print(f"YAML file exists: {os.path.exists(yaml_path)}")
    print("-" * 50)

    if not os.path.exists(yaml_path):
        # Look for sim.yaml in parent directories
        parent_dir = this_dir
        for _ in range(3):  # Look up to 3 levels up
            parent_dir = os.path.dirname(parent_dir)
            test_path = os.path.join(parent_dir, "sim.yaml")
            if os.path.exists(test_path):
                yaml_path = test_path
                print(f"Found YAML file at: {yaml_path}")
                break
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Could not find sim.yaml in {yaml_path} or parent directories")

    if lss_pattern.match(mode):
        key = (mode, source)
        if key in yaml_lss_updates(mode=mode, source=source, exp=exp):
            yaml_changes = {f"simulation:{k}": v for k, v in yaml_lss_updates(mode=mode, source=source, exp=float(exp))[key].items()}
            update_yaml(yaml_path, yaml_changes)
        else:
            raise ValueError(f"Unsupported mode/source combination: {key}")
    else:
        raise ValueError("Unsupported mode(How did you even select that?)")
    cmd = [
        sys.executable,
        f"{this_dir}/python/run_recipes.py",
        f"--inputYAML={yaml_path}",
        "--outputDir", f"{fits_file_path}",
        "--doCalib=0",
        "--sequence=1",
        "--nCores=4"
    ]

    print("\nDebug: Package Configuration")
    print("-" * 50)
    print(f"Current package search paths:\n{sim.rc.__search_path__}")
    print(f"Local packages directory: {packages_path}")
    if os.path.exists(packages_path):
        print("Available packages:")
        for item in os.listdir(packages_path):
            if os.path.isdir(os.path.join(packages_path, item)):
                print(f"- {item}")
    else:
        print(f"Warning: Packages directory {packages_path} does not exist!")
    print("-" * 50)

    result = subprocess.run(cmd, stderr=sys.stderr, stdout=sys.stdout,check=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    return None