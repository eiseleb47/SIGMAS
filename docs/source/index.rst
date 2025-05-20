.. SIGMAS documentation master file, created by
   sphinx-quickstart on Wed May 14 19:03:55 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the SIGMAS documentation
===================================

Sigmas is a basic web server based simulation dashboard. It utilizes the simulation capabilities of `ScopeSim <https://github.com/AstarVienna/ScopeSim>`_ and `ScopeSim_Templates <https://github.com/AstarVienna/ScopeSim_Templates>`_.
The local web server is hosted using `Flask <https://flask.palletsprojects.com/en/stable/>`_.

Installation
------------
.. code-block::
   
   (.venv) $ pip install sigmas

Usage
-----

To start the server and open a new tab in your default Browser on the root page of the dashboard simply run:
.. code-block::

   (.venv) $ sigmas

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   sim
   flask
   api