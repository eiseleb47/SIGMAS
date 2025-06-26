from astrodonut.donut import Donut
from astrodonut.donut_List import DonutList
from astrodonut.donut_exporter import DonutExporter
import scopesim as sim
from .utils import ensure_packages_installed
from astropy.io import fits
from astropy import units as u
from synphot.models import BlackBody1D
from synphot import SourceSpectrum

import tempfile, os
from pathlib import Path

def create_one_donut(values: dict, pkg_path=''):
    """
    Create a Donut source and then run it through a scopesim Optical Train.
    
    :param values: A dictionary containing the parameters of the Donut.
    :type values: dict
    :return: The path to the created fits file
    :rtype: str
    """
    temp_dir = tempfile.gettempdir()
    fits_path = Path(temp_dir) / "simulation_result"
    fits_dir = Path(fits_path)
    donut_path = fits_dir / "donut.fits"
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
        export_ring1.save_to_fits(donut_path, overwrite=True)

        if len(pkg_path) == 0:
            pkg_path = Path.home() / '.inst_pkgs'

        ensure_packages_installed(file_path=pkg_path)

        sim.rc.__config__["!SIM.file.local_packages_path"] = pkg_path

        cmds = sim.UserCommands(use_instrument="METIS", set_modes=['img_lm'], properties={"!OBS.exptime": 3600})

        metis = sim.OpticalTrain(cmds)

        metis['skycalc_atmosphere'].include=False
        metis['detector_linearity'].include=False
        metis['quantization'].include=False

        hdu = fits.open(donut_path)
        hdu[0].data /= hdu[0].data.max()
        hdu[0].header["CDELT1"] = (0.0057 / 3600)   #CD1_1 
        hdu[0].header["CDELT2"] = (0.0057 / 3600)   #CD2_2 #für metis 0.0057 / 3600
        hdu[0].header["CRVAL1"] = 0
        hdu[0].header["CRVAL2"] = 0
        hdu[0].header["CRPIX1"] = 1000.5 #(Naxis +1) /2
        hdu[0].header["CRPIX2"] = 1000.5
        hdu[0].header["CUNIT1"] = "deg"
        hdu[0].header["CUNIT2"] = "deg"

        emission_raw = SourceSpectrum(BlackBody1D, temperature=150 * u.K)*5e-11

        metis.observe(sim.Source(image_hdu=hdu[0], spectra=emission_raw))
        result = metis.readout(detector_readout_mode="auto")[0]
        result.writeto(fits_dir / 'finished_donut.fits', overwrite=True)

        return str(donut_path)
    
    except (ValueError, KeyError) as e:
        raise ValueError(f"Simulation failed: {str(e)}")