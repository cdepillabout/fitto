#!/usr/bin/env python2
import sys
from fitto import app

host='0.0.0.0'
debug=False

if '-d' in sys.argv or '--debug' in sys.argv:
    debug=True

app.run(debug=debug, host=host)
