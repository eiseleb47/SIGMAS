Simulations
===========
Currently there are three functions supporting Simulations. The explanations below assume they are used in a python script or environment and do **NOT** reflect their implementation or versatility in the use case of the GUI.

Direct Simulation
-----------------
Direct Simulations are closest to the underlying ScopeSim code. They have a small amount of changeable parameters, however they feed directly into the simulation engine without any layer in between. Theoretically every mode currently supported ScopeSim can be used.

.. autofunction:: sigmas.simulations.sim.Simulate

Yaml file Simulation
--------------------
The yaml Simulations make use of the approach first implemented in the `METIS_Simulations <https://github.com/AstarVienna/METIS_Simulations>`_ Repository. They support a similar amount of parameters to the direct Simulations, however they work with a lot of ScopeSim parameters that are specific to METIS which have been set in the background. Thus these are most likely closer to science grade Simulations.

.. autofunction:: sigmas.simulations.run_sim.Simulate

Donut Simulation
----------------
The Donut Simulations support a different type of Simulation. They make use of the `AstroDonut <https://github.com/Tearyt/AstroDonut>`_ Package. These aim to simulate '...synthetic elliptical ring structures...'.

.. autofunction:: sigmas.simulations.donut_sim.create_one_donut