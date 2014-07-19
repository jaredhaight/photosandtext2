import os
import sys
sys.path.append(os.getcwd())
from photosandtext2 import app
from photosandtext2 import views

if __name__ == "__main__":
    if not app.debug:
        import logging
        logging.basicConfig(filename='..\pat2.log',level=logging.DEBUG)
    app.run()