from pathlib import Path
import tempfile
import yaml
import os
from sigmas.simulations.utils import (
    get_scopesim_inst_pkgs_path,
    ensure_packages_installed,
    save_fits,
    update_yaml
)
def test_get_scopesim_inst_pkgs_path(Path=Path.home()):
    path = get_scopesim_inst_pkgs_path(Path)
    assert os.path.exists(path)

def test_update_yaml_creates_nested_keys():
    with tempfile.NamedTemporaryFile("w+", suffix=".yaml", delete=False) as tf:
        yaml.dump({"a": {"b": 1}}, tf)
        tf.flush()
        update_yaml(tf.name, {"a:c": 2})
        tf.seek(0)
        data = yaml.safe_load(tf)
        assert data["a"]["c"] == 2
