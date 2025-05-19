import os
import tempfile
from .simulations.run_sim import Simulate
from .simulations.donut import donut
import pathlib
import re

from flask import Flask, render_template, request, flash, send_file, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '9936c5876875aca8448c987732b762753fa8ce09dc5df172128ab28d92178544'

    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('welcome.html')
    
    @app.route('/lss', methods=['GET', 'POST'])
    def lss():
        return render_template('lss.html')
    
    @app.route('/img', methods=['GET', 'POST'])
    def img():
        return render_template('img.html')

    @app.route('/simulation', methods=['POST'])
    def sim():
        if request.method == 'POST':
            lss_pattern = re.compile("lss_[lnm]")
            img_pattern = re.compile("img_[lnm]")
            
            variables = {
            "mode": request.form.get('mode'),
            "source": request.form.get('source'),
            "exposure_time": request.form.get('exposure_time')}

            if not variables['exposure_time']:
                flash('Please enter an exposure time!')
                if lss_pattern.match(variables['mode']):
                    return render_template('lss.html')
                elif img_pattern.match(variables['mode']):
                    return render_template('img.html')

            try:
                Simulate(variables=variables)

                if lss_pattern.match(variables['mode']):
                    return render_template('lss.html', fits_url=url_for('display_fits'), src=variables["source"], mode=variables["mode"])
                if img_pattern.match(variables['mode']):
                    return render_template('img.html', fits_url=url_for('display_fits'), src=variables["source"], mode=variables["mode"])

            except Exception as e:
                flash(f'Simulation failed: {str(e)}')
                return redirect(url_for('home'))

        return render_template('welcome.html')
    @app.route('/display_fits', methods=['POST', 'GET'])
    def display_fits():
        temp_dir = tempfile.gettempdir()
        fits_path = os.path.join(temp_dir, "simulation_result")
        fits_dir = pathlib.Path(fits_path)
        latest = max(fits_dir.glob("*.fits"), key=lambda p: p.stat().st_mtime)
        filename = str(latest)
        file_path = os.path.join(fits_dir, filename)
        if not os.path.exists(filename):
            print("FITS file not found in /display_fits route!")
            return "FITS file not found", 404
        return send_file(file_path, mimetype='image/fits')
    
    @app.route('/secret', methods=['POST', 'GET'])
    def secret():
        return render_template('donut.html')
    
    @app.route('/donut_sim', methods=['POST', 'GET'])
    def donut_sim():
        if request.method == 'POST':
            values = {
            "semi-maj": request.form.get('Semi-major axis'),
            "semi-min": request.form.get('Semi-minor axis'),
            "ecc": request.form.get('Eccentricity'),
            "inc": request.form.get('Inclination'),
            "width": request.form.get('Width'),
            "height": request.form.get('Height')}
        return render_template('secret_donut.html')
    return app