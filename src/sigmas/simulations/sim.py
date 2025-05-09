import scopesim as sim
import scopesim_templates
from scopesim_templates.stellar.clusters import cluster
from scopesim_templates.extragalactic.galaxies import elliptical
from astropy import units as u
from astropy.io import fits
from .utils import get_scopesim_inst_pkgs_path, ensure_packages_installed
from .utils import starFieldM, starFieldX, starFieldY, starFieldT

def Simulate(mode: str, exp: float, object=None, fits=None, input_file=None):
    """
    Simulate the observation of a source with the specified mode and exposure time.
    
    Parameters:
    - mode: The mode of observation (e.g., "lss_l").
    - exp: The exposure time in seconds.
    - source_flux: The flux of the source.
    
    Returns:
    - hdu: The observed data.
    """
    
    # Set up the simulation
    sim.rc.__config__["!SIM.file.local_packages_path"] = get_scopesim_inst_pkgs_path()

    ensure_packages_installed()

    cmds = sim.UserCommands(use_instrument="METIS", set_modes=[mode])
    cmds["!OBS.dit"] = float(exp)/4
    cmds["!OBS.ndit"] = 4
    cmds["!DET.width"] = 4096
    cmds["!DET.height"] = 4096
    # TODO Add support for Eso keywords here

    metis = sim.OpticalTrain(cmds)

    metis["skycalc_atmosphere"].include = False
    metis["telescope_reflection"].include = False

    if object is not None:
        if object == "Star Field":
            src = scopesim_templates.stellar.stars(
                amplitudes = starFieldM,
                x = starFieldX,
                y = starFieldY,
                filter_name = "Ks",
                spec_types = starFieldT
            )
        if object == "Elliptical Galaxy":
            src = elliptical(
            sed = "brown/NGC4473",
            z = 0,
            amplitude = 5,
            filter_name = "Ks",
            pixel_scale = 0.1,
            half_light_radius = 30,
            n = 4,
            ellip = 0.5,
            ellipticity = 0.5,
            angle = 30,
            )
    else:
        return "No object provided"
    
    #src = laser_spectrum_lm(
    #    specdict={
    #        "wave_min" : 2.7,
    #        "wave_max" : 4.3,
    #        "spectral_bin_width" : 0.0001,
    #        "wave_unit" : u.um,
    #    }
    #)

    # From fits file
    # src = sim.Source(image_hdu=input_file)

    metis.observe(src, update=True)

    hdu = metis.readout(detector_readout_mode="auto")[0]
    return hdu