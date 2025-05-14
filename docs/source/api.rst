API
===

To run a simulation by hand or include it in other python code you can use the ``sigmas.simulations.sim.Simulate()`` function:

.. autofunction:: sigmas.simulations.sim.Simulate

Utils
-----

Utility functions used in other scripts.

.. autofunction:: sigmas.simulations.utils.get_scopesim_inst_pkgs_path
.. autofunction:: sigmas.simulations.utils.save_fits
.. autofunction:: sigmas.simulations.utils.ensure_packages_installed

Flask
-----

A function to call the *app factory* to create multiple instances of the app.

.. autofunction:: sigmas.__init__.create_app