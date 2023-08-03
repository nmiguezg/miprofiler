#!/usr/bin/env python
import flask

from modaresi.profilers import Modaresi_profiler


app = flask.Flask(__name__)
app.config["DEBUG"] = True

moda = Modaresi_profiler()
@app.route('/profile', methods=['POST'])
def profile():
    
    data = flask.request.data
    
    return