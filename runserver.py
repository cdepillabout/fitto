#!/usr/bin/env python2
import sys
from fitto import app
import fitto.settings

host='0.0.0.0'
debug=None

if '-d' in sys.argv or '--debug' in sys.argv:
    debug=True

if '-n' in sys.argv or '--no-debug' in sys.argv:
    debug=False

app.config.from_object('fitto.settings')

if debug is not None:
    app.run(debug=debug, host=host)
else:
    app.run(host=host)
