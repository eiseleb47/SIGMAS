import os
import tempfile
from pathlib import Path
from simulations.sim import Simulate

from flask import Flask, render_template, request, flash, send_file, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '9936c5876875aca8448c987732b762753fa8ce09dc5df172128ab28d92178544'

    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('index.html')

    @app.route('/simulation', methods=['POST'])
    def sim():
        flash('Simulation is running...')
        if request.method == 'POST':
            exposure_time = request.form.get('exposure_time')
            if not exposure_time:
                flash('Please enter an exposure time')
                return render_template('index.html')
            variables = {
            "mode": request.form.get('mode'),
            "source": request.form.get('source'),
            "exposure_time": exposure_time#float(request.form.get('exposure_time'))
            }

            try:
                hdu = Simulate(variables["mode"], variables["exposure_time"], variables["source"])
                flash('Simulation finished successfully!')
            except Exception as e:
                flash(f'Simulation failed: {str(e)}')
                return redirect(url_for('home'))

        return render_template('index.html')
    
    return app