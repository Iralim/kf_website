import sys
import os

# путь к проекту Flask
sys.path.insert(0, "/var/www/u3360972/data/kf")

INTERP = "/var/www/u3360972/data/flaskenv/bin/python"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

from run import app as application


# import sys
# import os
#
# INTERP = os.path.expanduser("/var/www/u3360972/data/flaskenv/bin/python")
# if sys.executable != INTERP:
#    os.execl(INTERP, INTERP, *sys.argv)
#
# sys.path.append(os.getcwd())
#
# from run import application