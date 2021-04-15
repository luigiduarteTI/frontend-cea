#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/DashApp/")
# server é a variável server do arquivo "DashApp/DashApp/__init__.py"
from DashApp import server as application

