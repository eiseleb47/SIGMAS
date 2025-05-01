from simulations.sim import Simulate
from astropy.io import fits
import os

def test_hdu():
    mode = "lss_l"
    exp = 300
    object = "star"
    result = Simulate(mode, exp, object)

    assert result==fits.hdu.image.PrimaryHDU or fits.hdu.image.ImageHDU

def test_simulations_folder_exists():

    repo_root = os.path.abspath(os.path.dirname(__file__) + "/..")
    sims_path = os.path.join(repo_root, "simulations")
    assert os.path.isdir(sims_path), f"'simulations' folder not found at {sims_path}"