#!/usr/bin/env bash
source /home/kali/.environments/sigmas/bin/activate

flask --app sigmas run && python "$(dirname "$0")/sigmas/run_app.py"