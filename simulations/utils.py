from pathlib import Path
import importlib.util
from astropy.io import fits

def get_scopesim_inst_pkgs_path():
    """Find the inst_pkgs directory relative to scopesim installation"""
    package_path = str(Path(__file__).parent / "inst_pkgs")
    # Look for inst_pkgs in parent directories
    return package_path if Path(package_path).exists() else None

def save_fits(file, path=""):
    '''Save a fits file to disk'''
    file.writeto(path + "output.fits", overwrite=True)
    return None