from astrodonut.donut import Donut
from astrodonut.donut_List import DonutList
from astrodonut.donut_exporter import DonutExporter

import tempfile, os
from pathlib import Path

def create_one_donut(values: dict):
    """
    Create a Donut source and then run it through a scopesim Optical Train.
    
    :param values: A dictionary containing the parameters of the Donut.
    :type values: dict
    :return: The path to the created fits file
    :rtype: str
    """
    temp_dir = tempfile.gettempdir()
    fits_path = os.path.join(temp_dir, "simulation_result")
    fits_dir = Path(fits_path)
    donut_path = Path.joinpath(fits_dir, "donut.fits")
    if not os.path.exists(fits_dir):
        os.mkdir(fits_dir)

    try:
        # Create donut with parameter validation
        donut = Donut(
            a1=float(values["semi-maj"]),
            b1=float(values["semi-min"]),
            ecc=float(values["ecc"]),
            inc=float(values["inc"]),
            ring_ratio=float(values["ring_ratio"]),
            width=int(values["width"]),
            height=int(values["height"])
        )
        
        donut.ring()

        export_ring1 = DonutExporter(donut)
        export_ring1.save_to_fits(str(donut_path), overwrite=True)

        return str(donut_path)
    
    except (ValueError, KeyError) as e:
        raise ValueError(f"Simulation failed: {str(e)}")