"""
Usage: >python run_network.py [network_dir] [optl port]
Optional input directory path to the 'network' output directory of sigmajs exporter

By Lynn Cherny (@arnicas)
This file takes the network directory output from the Gephi
SigmaJS exporter and fixes some settings in the config.json,
then starts a simpleserver for the files.
"""

import json
import os
import SimpleHTTPServer
import SocketServer
import sys


try:
    dir = sys.argv[1]
except:
    dir = 'network'

try:
    PORT = int(sys.argv[2])
except:
    PORT = 8000

try:
    os.chdir(dir)
except:
    print "Can't change to a sigmajs export network directory here...!"
    sys.exit()

with open('config.json', 'r') as handle:
    data = json.load(handle)
    old = data

data["sigma"]["graphProperties"]["minEdgeSize"] = 1
data["sigma"]["graphProperties"]["maxNodeSize"] = 20
data["sigma"]["graphProperties"]["maxEdgeSize"] = 8
data["sigma"]["graphProperties"]["minNodeSize"] = 7
data["sigma"]["drawingProperties"]["labelThreshold"] = 10

with open('config_old.json', 'w') as handle:
    json.dump(old, handle)

with open('config.json', 'w') as handle:
    json.dump(data, handle)

print "Fixed network/config.json, now starting server...."

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Now serving at port", PORT
print "Load your file by using 'localhost:" + str(PORT)+ "' in the browser."
httpd.serve_forever()