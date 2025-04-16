import scopesim as sim
from scopesim.source import laser_spectrum_lm
from astropy import units as u

mode = "lms"
exposure_time = 100

sim.rc.__config__["!SIM.file.local_packages_path"] = "/home/kali/Documents/Play_With_Scope_Sim/inst_pkgs"

cmds = sim.UserCommands(use_instrument="METIS", set_modes=[mode])
cmds["!OBS.dit"] = exposure_time
cmds["!DET.width"] = 4096
cmds["!DET.height"] = 4096

metis = sim.OpticalTrain(cmds)

metis["skycalc_atmosphere"].include = False
metis["telescope_reflection"].include = False

src = laser_spectrum_lm(
    specdict={
        "wave_min" : 2.7,
        "wave_max" : 4.3,
        "spectral_bin_width" : 0.0001,
        "wave_unit" : u.um,
    }
)

metis.observe(src, update=True)

hdu = metis.readout(detector_readout_mode="auto")[0]