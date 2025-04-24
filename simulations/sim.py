import scopesim as sim
from scopesim_templates.stellar.clusters import cluster
from scopesim_templates.extragalactic.galaxies import elliptical
from astropy import units as u
from astropy.io import fits
from simulations.utils import get_scopesim_inst_pkgs_path

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

    cmds = sim.UserCommands(use_instrument="METIS", set_modes=[mode])
    cmds["!OBS.dit"] = float(exp)
    cmds["!DET.width"] = 4096
    cmds["!DET.height"] = 4096

    metis = sim.OpticalTrain(cmds)

    metis["skycalc_atmosphere"].include = False
    metis["telescope_reflection"].include = False

    if object is not None:
        if object == "star":
            src = cluster(
            )
        if object == "agn":
            src = elliptical(
                r_eff=1,
                filter_name="Ks",
                pixel_scale=0.01,
                amplitude=1E15
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
    
    # Add support for Eso keywords here

    #hdu.writeto("output.fits", overwrite=True)
    #print(hdu[0])
    return hdu