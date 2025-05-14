import tempfile
import os
from .utils import update_yaml

def simulate(variables):
    temp_dir = tempfile.gettempdir()
    fits_file_path = os.path.join(temp_dir, "simulation_result.fits")
    mode, source, exp = variables["mode"], variables["source"], variables["exposure_time"] 

    if mode == "lss_n" or mode == "lss_m":
        print("yes")