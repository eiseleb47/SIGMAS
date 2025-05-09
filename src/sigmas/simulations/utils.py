from pathlib import Path
from astropy.io import fits
import numpy as np
import logging
import scopesim as sim
import os

def get_scopesim_inst_pkgs_path():
    """Find the inst_pkgs directory relative to scopesim installation"""
    package_dir = Path(__file__).parent / "inst_pkgs"
    package_dir.mkdir(exist_ok=True, parents=True)
    
    if not package_dir.exists():
        raise RuntimeError(f"Failed to create directory: {package_dir}")
    if not os.access(package_dir, os.W_OK):
        raise RuntimeError(f"Directory not writable: {package_dir}")
        
    return str(package_dir)

def save_fits(file, path=""):
    '''Save a fits file to disk'''
    file.writeto(path + "output.fits", overwrite=True)
    return None

def ensure_packages_installed():
       """Ensure required packages are installed"""

       required_packages = ["Armazones", "ELT", "METIS"]
       pkg_path = get_scopesim_inst_pkgs_path()

       if  not all(Path(pkg_path, pkg).is_dir() for pkg in required_packages):

              try:
                     for pkg in required_packages:
                            sim.download_packages([pkg])
              except Exception as e:
                     raise
       return None

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