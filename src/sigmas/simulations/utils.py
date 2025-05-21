from astropy.io import fits
import numpy as np
import scopesim as sim
import os
import yaml
from pathlib import Path
def get_scopesim_inst_pkgs_path():
    """Get the path to the instrument packages directory."""
    pkg_path = os.getenv("SCOPESIM_INST_PKGS")
    if pkg_path and os.path.exists(pkg_path):
        return os.path.abspath(pkg_path)
    
    file = Path(__file__)
    parent = file.parent
    filepath = os.path.join(parent, "inst_pkgs")
    if os.path.exists(filepath):
        return os.path.abspath(filepath)
        
    home = os.path.expanduser("~")
    home_inst_pkgs = os.path.join(home, ".scopesim/inst_pkgs")
    if os.path.exists(home_inst_pkgs):
        return os.path.abspath(home_inst_pkgs)
        
    # Create default location if nothing exists
    os.makedirs(filepath)
    return os.path.abspath(filepath)

def save_fits(file, path=""):
    '''Save a fits file to disk.

    :param file: Path of the fits file to write to disk.
    :type file: str
    :param path: Path to the location where the file should be saved.
    :type path: str
    :rtype: None
    '''
    file.writeto(path + "output.fits", overwrite=True)
    return None

def ensure_packages_installed():
    """Ensure required packages are installed"""
    required_packages = [
        "Armazones",
        "ELT", 
        "METIS"
    ]
    pkg_path = get_scopesim_inst_pkgs_path()
    
    print(f"Installing packages to: {pkg_path}")
    
    for pkg in required_packages:
        try:
            if not os.path.exists(os.path.join(pkg_path, pkg)):
                print(f"Installing {pkg}")
                sim.download_packages(pkg)
            else:
                print(f"Found existing {pkg} installation")
        except Exception as e:
            print(f"Failed to install {pkg}: {str(e)}")
            raise RuntimeError(f"Package installation failed: {str(e)}")
    
    return True

def update_yaml(file, changes):
    def set_nested(data, key_path, value):
        for key in key_path[:-1]:
            if key not in data or not isinstance(data[key], dict):
                data[key] = {}
            data = data[key]
        data[key_path[-1]] = value

    with open(file, 'r') as f:
        data = yaml.safe_load(f)

    for dotted_key, value in changes.items():
        key_path = dotted_key.split(':')
        set_nested(data, key_path, value)

    with open(file, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
    return

def yaml_lss_updates(mode, source, exp):
        return{
        # LSS mode updates
        ("lss_l", "simple_gal"): {"do.catg": "LM_LSS_SCI_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "L_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,LM", "properties:type": "OBJECT"},
        ("lss_l", "empty_sky"): {"do.catg": "LM_LSS_SKY_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "L_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,LM", "properties:type": "SKY"},
        ("lss_l", "simple_star8"): {"do.catg": "LM_LSS_STD_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "L_spec", "properties:catg": "CALIB", "properties:tech": "LSS,LM", "properties:type": "STD"},
        ("lss_n", "simple_gal"): {"do.catg": "N_LSS_SCI_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,N", "properties:type": "OBJECT"},
        ("lss_n", "empty_sky"): {"do.catg": "N_LSS_SKY_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N_spec", "properties:catg": "SCIENCE", "properties:tech": "LSS,N", "properties:type": "SKY"},
        ("lss_n", "simple_star8"): {"do.catg": "N_LSS_STD_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N_spec", "properties:catg": "CALIB", "properties:tech": "LSS,N", "properties:type": "STD"},
        # IMG mode updates
        ("img_lm", "simple_star12"): {"do.catg": "LM_IMAGE_STD_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "Lp", "properties:catg": "CALIB", "properties:tech": "IMAGE,LM", "properties:type": "STD"},
        ("img_lm", "empty_sky"): {"do.catg": "LM_IMAGE_SKY_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "Lp", "properties:catg": "CALIB", "properties:tech": "IMAGE,LM", "properties:type": "SKY"},
        ("img_lm", "star_field"): {"do.catg": "LM_IMAGE_SCI_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "Lp", "properties:catg": "SCIENCE", "properties:tech": "IMAGE,LM", "properties:type": "OBJECT"},
        ("img_n", "simple_star12"): {"do.catg": "N_IMAGE_STD_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N1", "properties:catg": "CALIB", "properties:tech": "IMAGE,N", "properties:type": "STD"},
        ("img_n", "empty_sky"): {"do.catg": "N_IMAGE_SKY_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N1", "properties:catg": "CALIB", "properties:tech": "IMAGE,N", "properties:type": "SKY"},
        ("img_n", "star_field"): {"do.catg": "N_IMAGE_SCI_RAW", "mode": mode, "source:name": source, "properties:dit": exp, "properties:filter_name": "N1", "properties:catg": "SCIENCE", "properties:tech": "IMAGE,N", "properties:type": "OBJECT"},
        }

# Arrays used in star fields template
# For now taken from Metis_Simulations
starFieldX = np.array([-8.15592743,  7.01303926,  8.01500244,  1.87226377,  6.97505972,
       -7.33994824,  0.04191974,  5.35931242,  8.40940718, -0.49102622,
        4.58550425,  6.10882803, -1.99466201, -9.72891962, -3.65611485,
       -1.20411157, -2.02697232,  8.42325234, -5.67781285,  8.68952776])


starFieldY = np.array([ 9.583468  , -5.65889576,  7.44908775,  4.17753575,  4.43878784,
        1.18114661,  5.65337934, -6.90408802, -0.49683094,  6.04866284,
        8.58989225,  8.85721093,  0.7475543 , -1.90119023,  4.98409528,
       -0.96123847,  9.34819477,  9.42408694,  8.20907011, -1.03093753])


starFieldM = np.array([13.9583468 , 12.43411042, 13.74490878, 13.41775357, 13.44387878,
       13.11811466, 13.56533793, 12.3095912 , 12.95031691, 13.60486628,
       13.85898923, 13.88572109, 13.07475543, 12.80988098, 13.49840953,
       12.90387615, 13.93481948, 13.94240869, 13.82090701, 12.89690625])

starFieldT = ["A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V","A0V"]