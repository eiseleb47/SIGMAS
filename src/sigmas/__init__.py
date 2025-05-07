import os
import tempfile
from pathlib import Path
from .simulations.sim import Simulate
from .simulations.utils import save_fits
from astropy.io import fits

from flask import Flask, render_template, request, flash, send_file, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '9936c5876875aca8448c987732b762753fa8ce09dc5df172128ab28d92178544'

    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('index.html')

    @app.route('/simulation', methods=['POST'])
    def sim():
        if request.method == 'POST':
            exposure_time = request.form.get('exposure_time')
            if not exposure_time:
                flash('Please enter an exposure time')
                return render_template('index.html')
            variables = {
            "mode": request.form.get('mode'),
            "source": request.form.get('source'),
            "exposure_time": exposure_time}

            try:
                hdu = Simulate(variables["mode"], variables["exposure_time"], variables["source"])

                temp_dir = tempfile.gettempdir()
                fits_file_path = os.path.join(temp_dir, "simulation_result.fits")
                hdu.writeto(fits_file_path, overwrite=True)

                if os.path.exists(fits_file_path):
                    print(f"FITS file created at: {fits_file_path}")
                else:
                    print("FITS file was not created!")

                flash('Simulation completed successfully!')

                return render_template('index.html', fits_url=url_for('display_fits'), src=variables["source"], mode=variables["mode"])

            except Exception as e:
                flash(f'Simulation failed: {str(e)}')
                return redirect(url_for('home'))

        return render_template('index.html')
    @app.route('/display_fits', methods=['POST', 'GET'])
    def display_fits():
        temp_dir = tempfile.gettempdir()
        fits_path = os.path.join(temp_dir, "simulation_result.fits")
        if not os.path.exists(fits_path):
            print("FITS file not found in /display_fits route!")
            return "FITS file not found", 404
        return send_file(fits_path, mimetype='image/fits')
    return app