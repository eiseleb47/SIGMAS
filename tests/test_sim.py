import pytest
from unittest.mock import Mock, patch
from sigmas.simulations.direct_sim import Simulate
from sigmas.simulations.run_sim import Yaml_Simulate
from astropy.io import fits
from subprocess import CompletedProcess
import os

def test_hdu():
    mode = "lss_l"
    exp = 300
    object = "Star Field"
    result = Simulate(mode, exp, object)

    assert isinstance(result, fits.HDUList)

def test_simulations_folder_exists():

    repo_root = os.path.dirname(os.path.dirname(__file__)) + "/src/sigmas/"
    sims_path = os.path.join(repo_root, "simulations")
    assert os.path.isdir(sims_path), f"'simulations' folder not found at {sims_path}"

# Test YAML simulation with valid parameters
def test_yaml_simulate_valid():
    test_variables = {
        "mode": "img_lm",
        "source": "simple_star12",
        "exposure_time": "300"
    }
    result = Yaml_Simulate(variables=test_variables)
    assert isinstance(result, type(CompletedProcess("test", None)))

# Test invalid parameters handling
def test_yaml_simulate_invalid():
    test_variables = {
        "mode": "invalid_mode",
        "source": "invalid_source",
        "exposure_time": "-1"
    }
    with pytest.raises(ValueError):
        Yaml_Simulate(variables=test_variables)

# Test mode pattern matching
def test_mode_pattern_matching():
    import re
    lss_pattern = re.compile("lss_[lnm]")
    img_pattern = re.compile("img_[lnm]")
    ifu_pattern = re.compile("lms")
    
    assert lss_pattern.match("lss_l")
    assert lss_pattern.match("lss_n")
    assert lss_pattern.match("lss_m")
    assert not lss_pattern.match("lss_x")
    
    assert img_pattern.match("img_l")
    assert ifu_pattern.match("lms")

def test_yaml_simulate_missing_keys():
    test_variables = {
        "mode": "lss_l"
        # missing 'source' and 'exposure_time'
    }
    with pytest.raises(Exception):
        Yaml_Simulate(variables=test_variables)

def test_simulate_invalid_mode():
    with pytest.raises(Exception):
        Simulate("invalid_mode", 100, "Star Field")