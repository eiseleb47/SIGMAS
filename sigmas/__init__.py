import os
import tempfile
from pathlib import Path
from ..simulations import Simulate

from flask import Flask, render_template, request, flash, send_file

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '9936c5876875aca8448c987732b762753fa8ce09dc5df172128ab28d92178544'

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            variables = {
            "mode": request.form.get('dropdown'),
            "exposure_time": request.form.get('exposure_time'),
            "flux": request.form.get('flux')}
            
        return render_template('index.html')
    
    return app