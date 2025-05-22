![Edited version of a conceptual drawing by ESO (https://elt.eso.org/instrument/METIS/)](https://github.com/user-attachments/assets/c8832d76-f818-46ea-ad73-00c0dc5a0efb)
# SIGMAS 
## Simulation Interface for Generating METIS Astronomical Spectra
## Summary
SIGMAS aims to simplify the creation of spectral simulations in different modes for the METIS instrument of the Extremely Large Telescope (ELT) using the [ScopeSim](https://github.com/AstarVienna/ScopeSim) package. This is done by providing a simple web based GUI that takes user input for multiple parameters, then performs the simulation locally and presents the created detector image.

It is intended for Astronomers or Students who are not familiar with the intricacies of ScopeSim and simply require basic simulated data without control over every parameter.

SIGMAS makes use of ScopeSim and it's dependencies as well as ScopeSim_Templates for the backend simulation and Flask as a framework for the web based GUI.
## Requirements
- ```ScopeSim```

- ```ScopeSim_Templates```

- ```Flask```

- ```Astropy```

- ```Numpy```
## User Stories
- As a university student, I want to create and look at simulated spectrographic data so that I can understand better how an Echelle Spectrograph works.
- As a software engineer working on the data reduction pipeline for the METIS instrument, I want to create my own simulation data, so that I can test my pipeline in different use cases.
- As an amateur astronomer using an older laptop, I want to limit the resolution and complexity of the simulations so that I can still use the tool without my system becoming unresponsive.
- As a user trying to load a previously saved simulation setup, I want the GUI to notify me if the input file is incomplete or contains errors, so that I can correct the issue without the program crashing or producing invalid results.
## Examples
After installing the package the GUI can be simply started from the terminal:
```bash
# Install sigmas from Pypi
pip install sigmas
# Run the webserver and open a new browser tab
sigmas
```
